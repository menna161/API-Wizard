from imports import *
from utils import *


def fit(self, trainloader, validloader, epochs=2, print_every=10, validate_every=1, save_best_every=1):
    optim_path = Path(self.best_model_file)
    optim_path = ((optim_path.stem + '_optim') + optim_path.suffix)
    with mlflow.start_run() as run:
        for epoch in range(epochs):
            self.model = self.model.to(self.device)
            mlflow.log_param('epochs', epochs)
            mlflow.log_param('lr', self.optimizer.param_groups[0]['lr'])
            mlflow.log_param('bs', trainloader.batch_size)
            print('Epoch:{:3d}/{}\n'.format((epoch + 1), epochs))
            epoch_train_loss = self.train_((epoch, epochs), trainloader, self.criterion, self.optimizer, print_every)
            if (validate_every and ((epoch % validate_every) == 0)):
                t2 = time.time()
                eval_dict = self.evaluate(validloader)
                epoch_validation_loss = eval_dict['final_loss']
                epoch_psnr = eval_dict['psnr']
                mlflow.log_metric('Train Loss', epoch_train_loss)
                mlflow.log_metric('Valdiation Loss', epoch_validation_loss)
                mlflow.log_metric('Valdiation PSNR', epoch_psnr)
                time_elapsed = (time.time() - t2)
                if (time_elapsed > 60):
                    time_elapsed /= 60.0
                    measure = 'min'
                else:
                    measure = 'sec'
                print((('\n' + ('/' * 36)) + f'''
{time.asctime().split()[(- 2)]}
Epoch {(epoch + 1)}/{epochs}
Validation time: {time_elapsed:.6f} {measure}
Epoch validation psnr: {epoch_psnr:.6f}
Epoch training loss: {epoch_train_loss:.6f}
Epoch validation loss: {epoch_validation_loss:.6f}'''))
                print((('\\' * 36) + '\n'))
                if ((self.best_validation_loss == None) or (epoch_validation_loss <= self.best_validation_loss)):
                    print('\n**********Updating best validation loss**********\n')
                    if (self.best_validation_loss is not None):
                        print('Previous best: {:.7f}'.format(self.best_validation_loss))
                    print('New best loss = {:.7f}\n'.format(epoch_validation_loss))
                    print((('*' * 49) + '\n'))
                    self.best_validation_loss = epoch_validation_loss
                    mlflow.log_metric('Best Loss', self.best_validation_loss)
                    optim_path = Path(self.best_model_file)
                    optim_path = ((optim_path.stem + '_optim') + optim_path.suffix)
                    torch.save(self.model.state_dict(), self.best_model_file)
                    torch.save(self.optimizer.state_dict(), optim_path)
                    mlflow.pytorch.log_model(self, 'mlflow_logged_models')
                    curr_time = str(datetime.now())
                    curr_time = ('_' + curr_time.split()[1].split('.')[0])
                    mlflow_save_path = (Path('mlflow_saved_training_models') / (Path(self.best_model_file).stem + '_{}'.format((str(epoch) + curr_time))))
                    mlflow.pytorch.save_model(self, mlflow_save_path)
                self.train()
    torch.cuda.empty_cache()
    print('\nLoading best model\n')
    self.model.load_state_dict(torch.load(self.best_model_file))
    self.optimizer.load_state_dict(torch.load(optim_path))
    os.remove(self.best_model_file)
    os.remove(optim_path)
