import time
import torch
from lib.Utility.metrics import AverageMeter
from lib.Utility.metrics import accuracy
import lib.Training.augmentation as augmentation
from lib.Training.augmentation import blur_data


def train(Dataset, model, criterion, epoch, optimizer, writer, device, args):
    '\n    Trains/updates the model for one epoch on the training dataset.\n\n    Parameters:\n        Dataset (torch.utils.data.Dataset): The dataset\n        model (torch.nn.module): Model to be trained\n        criterion (torch.nn.criterion): Loss function\n        epoch (int): Continuous epoch counter\n        optimizer (torch.optim.optimizer): optimizer instance like SGD or Adam\n        writer (tensorboard.SummaryWriter): TensorBoard writer instance\n        device (str): device name where data is transferred to\n        args (dict): Dictionary of (command line) arguments.\n            Needs to contain print_freq (int) and log_weights (bool).\n    '
    class_losses = AverageMeter()
    recon_losses = AverageMeter()
    if args.introspection:
        kld_real_losses = AverageMeter()
        kld_fake_losses = AverageMeter()
        kld_rec_losses = AverageMeter()
        criterion_enc = criterion[0]
        criterion_dec = criterion[1]
        optimizer_enc = optimizer[0]
        optimizer_dec = optimizer[1]
    else:
        kld_losses = AverageMeter()
    losses = AverageMeter()
    batch_time = AverageMeter()
    data_time = AverageMeter()
    top1 = AverageMeter()
    model.train()
    end = time.time()
    for (i, (inp, target)) in enumerate(Dataset.train_loader):
        if args.data_augmentation:
            inp = augmentation.augment_data(inp, args)
        inp = inp.to(device)
        target = target.to(device)
        recon_target = inp
        class_target = target
        if (args.denoising_noise_value > 0.0):
            noise = (torch.randn(inp.size()).to(device) * args.denoising_noise_value)
            inp = (inp + noise)
        if args.blur:
            inp = blur_data(inp, args.patch_size, device)
        data_time.update((time.time() - end))
        if args.introspection:
            (real_mu, real_std) = model.module.encode(inp)
            z = model.module.reparameterize(real_mu, real_std)
            class_output = model.module.classifier(z)
            recon = torch.sigmoid(model.module.decode(z))
            model.eval()
            (recon_mu, recon_std) = model.module.encode(recon.detach())
            model.train()
            z_p = torch.randn(inp.size(0), model.module.latent_dim).to(model.module.device)
            recon_p = torch.sigmoid(model.module.decode(z_p))
            model.eval()
            (mu_p, std_p) = model.module.encode(recon_p.detach())
            model.train()
            (cl, rl, kld_real, kld_rec, kld_fake) = criterion_enc(class_output, class_target, recon, recon_target, real_mu, real_std, recon_mu, recon_std, mu_p, std_p, device, args)
            kld_real_losses.update(kld_real.item(), inp.size(0))
            alpha = 1
            if (not args.gray_scale):
                alpha = 3
            loss_encoder = ((cl + (alpha * rl)) + (args.var_beta * (kld_real + ((0.5 * (kld_rec + kld_fake)) * args.gamma))))
            optimizer_enc.zero_grad()
            loss_encoder.backward()
            optimizer_enc.step()
            recon = torch.sigmoid(model.module.decode(z.detach()))
            model.eval()
            (recon_mu, recon_std) = model.module.encode(recon.detach())
            model.train()
            recon_p = torch.sigmoid(model.module.decode(z_p))
            model.eval()
            (fake_mu, fake_std) = model.module.encode(recon_p.detach())
            model.train()
            (rl, kld_rec, kld_fake) = criterion_dec(recon, recon_target, recon_mu, recon_std, fake_mu, fake_std, args)
            loss_decoder = (((0.5 * (kld_rec + kld_fake)) * args.gamma) + (rl * alpha))
            optimizer_dec.zero_grad()
            loss_decoder.backward()
            optimizer_dec.step()
            losses.update((loss_encoder + loss_decoder).item(), inp.size(0))
            class_losses.update(cl.item(), inp.size(0))
            recon_losses.update(rl.item(), inp.size(0))
            kld_rec_losses.update(kld_rec.item(), inp.size(0))
            kld_fake_losses.update(kld_fake.item(), inp.size(0))
            prec1 = accuracy(class_output, target)[0]
            top1.update(prec1.item(), inp.size(0))
            batch_time.update((time.time() - end))
            end = time.time()
            if ((i % args.print_freq) == 0):
                print('Training: [{0}][{1}/{2}]\tTime {batch_time.val:.3f} ({batch_time.avg:.3f})\tData {data_time.val:.3f} ({data_time.avg:.3f})\tLoss {loss.val:.4f} ({loss.avg:.4f})\tClass Loss {cl_loss.val:.4f} ({cl_loss.avg:.4f})\tPrec@1 {top1.val:.3f} ({top1.avg:.3f})\tRecon Loss {recon_loss.val:.4f} ({recon_loss.avg:.4f})\tKL {KLD_loss.val:.4f} ({KLD_loss.avg:.4f})'.format((epoch + 1), i, len(Dataset.train_loader), batch_time=batch_time, data_time=data_time, loss=losses, cl_loss=class_losses, top1=top1, recon_loss=recon_losses, KLD_loss=kld_real_losses))
        else:
            (class_samples, recon_samples, mu, std) = model(inp)
            if args.autoregression:
                recon_samples_autoregression = torch.zeros(recon_samples.size(0), inp.size(0), 256, inp.size(1), inp.size(2), inp.size(3)).to(device)
                for j in range(model.module.num_samples):
                    recon_samples_autoregression[j] = model.module.pixelcnn(recon_target, torch.sigmoid(recon_samples[j])).contiguous()
                recon_samples = recon_samples_autoregression
                recon_target = (recon_target * 255).long()
            (class_loss, recon_loss, kld_loss) = criterion(class_samples, class_target, recon_samples, recon_target, mu, std, device, args)
            loss = ((class_loss + recon_loss) + (args.var_beta * kld_loss))
            class_output = torch.mean(class_samples, dim=0)
            losses.update(((class_loss + recon_loss) + kld_loss).item(), inp.size(0))
            class_losses.update(class_loss.item(), inp.size(0))
            recon_losses.update(recon_loss.item(), inp.size(0))
            kld_losses.update(kld_loss.item(), inp.size(0))
            prec1 = accuracy(class_output, target)[0]
            top1.update(prec1.item(), inp.size(0))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            batch_time.update((time.time() - end))
            end = time.time()
            if ((i % args.print_freq) == 0):
                print('Training: [{0}][{1}/{2}]\tTime {batch_time.val:.3f} ({batch_time.avg:.3f})\tData {data_time.val:.3f} ({data_time.avg:.3f})\tLoss {loss.val:.4f} ({loss.avg:.4f})\tClass Loss {cl_loss.val:.4f} ({cl_loss.avg:.4f})\tPrec@1 {top1.val:.3f} ({top1.avg:.3f})\tRecon Loss {recon_loss.val:.4f} ({recon_loss.avg:.4f})\tKL {KLD_loss.val:.4f} ({KLD_loss.avg:.4f})'.format((epoch + 1), i, len(Dataset.train_loader), batch_time=batch_time, data_time=data_time, loss=losses, cl_loss=class_losses, top1=top1, recon_loss=recon_losses, KLD_loss=kld_losses))
    if args.introspection:
        writer.add_scalar('training/train_precision@1', top1.avg, epoch)
        writer.add_scalar('training/train_average_loss', losses.avg, epoch)
        writer.add_scalar('training/train_KLD_real', kld_real_losses.avg, epoch)
        writer.add_scalar('training/train_class_loss', class_losses.avg, epoch)
        writer.add_scalar('training/train_KLD_rec', kld_rec_losses.avg, epoch)
        writer.add_scalar('training/train_KLD_fake', kld_fake_losses.avg, epoch)
    else:
        writer.add_scalar('training/train_precision@1', top1.avg, epoch)
        writer.add_scalar('training/train_average_loss', losses.avg, epoch)
        writer.add_scalar('training/train_KLD', kld_losses.avg, epoch)
        writer.add_scalar('training/train_class_loss', class_losses.avg, epoch)
        writer.add_scalar('training/train_recon_loss', recon_losses.avg, epoch)
    print(' * Train: Loss {loss.avg:.5f} Prec@1 {top1.avg:.3f}'.format(loss=losses, top1=top1))
