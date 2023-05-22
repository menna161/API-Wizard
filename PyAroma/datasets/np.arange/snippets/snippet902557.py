from collections import Counter
import argparse
import numpy as np
import sys
import os
import json
import time
import random
import torch
import torch.nn as nn
from model import LinkPredictor
from reader import AtomicTSVReader, ConceptNetTSVReader, FB15kReader
import utils
import reader_utils
import evaluation_utils


def main(args):
    set_seeds(args.seed)
    if (args.dataset == 'FB15K-237'):
        dataset_cls = FB15kReader
        data_dir = 'data/FB15k-237/'
    elif (args.dataset == 'atomic'):
        dataset_cls = AtomicTSVReader
        data_dir = 'data/atomic/'
    elif (args.dataset == 'conceptnet'):
        dataset_cls = ConceptNetTSVReader
        data_dir = 'data/ConceptNet/'
    else:
        raise ValueError('Invalid option for dataset.')
    (train_data, valid_data, test_data, valid_labels, test_labels, train_network) = load_data(args.dataset, dataset_cls, data_dir, args.sim_relations)
    num_nodes = len(train_network.graph.nodes)
    num_rels = len(train_network.graph.relations)
    all_tuples = ((train_data.tolist() + valid_data.tolist()) + test_data.tolist())
    (all_e1_to_multi_e2, all_e2_to_multi_e1) = reader_utils.create_entity_dicts(all_tuples, num_rels, args.sim_relations)
    (train_e1_to_multi_e2, train_e2_to_multi_e1) = reader_utils.create_entity_dicts(train_data.tolist(), num_rels, args.sim_relations)
    (sim_train_e1_to_multi_e2, sim_train_e2_to_multi_e1) = reader_utils.create_entity_dicts(train_data.tolist(), num_rels)
    use_cuda = torch.cuda.is_available()
    if (use_cuda and (not args.no_cuda)):
        torch.cuda.set_device(args.gpu)
    cpu_decoding = args.cpu_decoding
    cpu_eval = (True if (args.dataset == 'atomic') else False)
    model = LinkPredictor(num_nodes, num_rels, args, use_cuda=use_cuda)
    graph_train_data = train_data
    (test_graph, test_rel, test_norm) = utils.build_test_graph(num_nodes, num_rels, graph_train_data)
    test_deg = test_graph.in_degrees(range(test_graph.number_of_nodes())).float().view((- 1), 1)
    test_node_id = torch.arange(0, num_nodes, dtype=torch.long).view((- 1), 1)
    test_rel = torch.from_numpy(test_rel).view((- 1), 1)
    test_norm = torch.from_numpy(test_norm).view((- 1), 1)
    if (use_cuda and (not args.no_cuda) and (not cpu_decoding)):
        test_node_id = test_node_id.cuda()
        test_norm = test_norm.cuda()
        test_rel = test_rel.cuda()
    valid_data = torch.LongTensor(valid_data)
    test_data = torch.LongTensor(test_data)
    if (use_cuda and (not args.no_cuda) and (not cpu_eval)):
        valid_data = valid_data.cuda()
        test_data = test_data.cuda()
    test_graph.ndata.update({'id': test_node_id, 'norm': test_norm})
    test_graph.edata['type'] = test_rel
    if (use_cuda and (not args.no_cuda)):
        model = model.cuda()
    model_state_file = get_model_name(args)
    if args.eval_only:
        if args.load_model:
            model_state_file = args.load_model
        else:
            print('Please provide model path for evaluation (--load_model)')
            sys.exit(0)
        checkpoint = torch.load(model_state_file)
        if (use_cuda and (not args.no_cuda) and cpu_eval):
            model.cpu()
            test_graph.ndata['id'] = test_graph.ndata['id'].cpu()
            test_graph.ndata['norm'] = test_graph.ndata['norm'].cpu()
            test_graph.edata['type'] = test_graph.edata['type'].cpu()
            model.decoder.no_cuda = True
        model.eval()
        model.load_state_dict(checkpoint['state_dict'])
        print(model)
        print('================DEV=================')
        mrr = evaluation_utils.ranking_and_hits(test_graph, model, valid_data, all_e1_to_multi_e2, train_network, fusion='graph-only', sim_relations=args.sim_relations, write_results=args.write_results, debug=args.debug)
        print('================TEST================')
        mrr = evaluation_utils.ranking_and_hits(test_graph, model, test_data, all_e1_to_multi_e2, train_network, fusion='graph-only', sim_relations=args.sim_relations, debug=args.debug)
        sys.exit(0)
    if os.path.isfile(model_state_file):
        print(model_state_file)
        overwrite = input('Model already exists. Overwrite? Y = yes, N = no\n')
        if (overwrite.lower() == 'n'):
            print('Quitting')
            sys.exit(0)
        elif (overwrite.lower() != 'y'):
            raise ValueError('Invalid Option')
    (adj_list, degrees, sparse_adj_matrix, rel) = utils.get_adj_and_degrees(num_nodes, num_rels, train_data)
    if args.sim_relations:
        sim_edge_ids = np.where((graph_train_data[(:, 1)] == (num_rels - 1)))[0]
        sampling_edge_ids = np.delete(np.arange(len(graph_train_data)), sim_edge_ids)
    else:
        sampling_edge_ids = None
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    forward_time = []
    backward_time = []
    print('Starting training...')
    epoch = 0
    best_mrr = 0
    while True:
        model.train()
        epoch += 1
        cur_train_data = graph_train_data[:]
        (g, node_id, edge_type, node_norm, data, labels) = utils.generate_sampled_graph_and_labels(cur_train_data, args.graph_batch_size, num_rels, adj_list, degrees, args.negative_sample, args.sim_sim, args.sim_relations, sim_train_e1_to_multi_e2, sampling_edge_ids)
        node_id_copy = np.copy(node_id)
        node_dict = {v: k for (k, v) in dict(enumerate(node_id_copy)).items()}
        node_id = torch.from_numpy(node_id).view((- 1), 1)
        edge_type = torch.from_numpy(edge_type)
        node_norm = torch.from_numpy(node_norm).view((- 1), 1)
        if (use_cuda and (not args.no_cuda)):
            node_id = node_id.cuda()
            (edge_type, node_norm) = (edge_type.cuda(), node_norm.cuda())
        g.ndata.update({'id': node_id, 'norm': node_norm})
        g.edata['type'] = edge_type
        batch_size = args.decoder_batch_size
        e1_keys = list(train_e1_to_multi_e2.keys())
        sub_e1_keys = {}
        (src, dst) = (np.concatenate((cur_train_data[(:, 0)], cur_train_data[(:, 2)])), np.concatenate((cur_train_data[(:, 2)], cur_train_data[(:, 0)])))
        rel = cur_train_data[(:, 1)]
        rel = np.concatenate((rel, (rel + num_rels)))
        cur_train_data = np.stack((src, rel, dst)).transpose()
        for e in cur_train_data:
            rel = e[1]
            if args.sim_relations:
                if ((rel == (num_rels - 1)) or (rel == ((num_rels * 2) - 1))):
                    continue
                elif (rel >= num_rels):
                    rel -= 1
            if ((e[0] in node_id_copy) and (e[2] in node_id_copy)):
                subgraph_src_idx = node_dict[e[0]]
                subgraph_tgt_idx = node_dict[e[2]]
                if ((subgraph_src_idx, rel) not in sub_e1_keys):
                    sub_e1_keys[(subgraph_src_idx, rel)] = [subgraph_tgt_idx]
                else:
                    sub_e1_keys[(subgraph_src_idx, rel)].append(subgraph_tgt_idx)
        key_list = list(sub_e1_keys.keys())
        random.shuffle(key_list)
        cum_loss = 0.0
        for i in range(0, len(key_list), batch_size):
            optimizer.zero_grad()
            graph_embeddings = model.get_graph_embeddings(g, epoch)
            model.decoder.cur_embedding = graph_embeddings
            batch = key_list[i:(i + batch_size)]
            if (len(batch) == 1):
                continue
            e1 = torch.LongTensor([elem[0] for elem in batch])
            rel = torch.LongTensor([elem[1] for elem in batch])
            e2 = [sub_e1_keys[(k[0], k[1])] for k in batch]
            batch_len = len(batch)
            if (use_cuda and (not args.no_cuda) and (not cpu_decoding)):
                target = torch.cuda.FloatTensor(batch_len, node_id_copy.shape[0]).fill_(0)
                e1 = e1.cuda()
                rel = rel.cuda()
            else:
                target = torch.zeros((batch_len, node_id_copy.shape[0]))
            for (j, inst) in enumerate(e2):
                target[(j, inst)] = 1.0
            target = (((1.0 - args.label_smoothing_epsilon) * target) + (1.0 / target.size(1)))
            if cpu_decoding:
                graph_embeddings = graph_embeddings.cpu()
                model.decoder.cpu()
                model.decoder.no_cuda = True
            t0 = time.time()
            loss = model.get_score(e1, rel, target, graph_embeddings)
            loss = torch.mean(loss)
            cum_loss += loss.cpu().item()
            t1 = time.time()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), args.grad_norm)
            optimizer.step()
            t2 = time.time()
            forward_time.append((t1 - t0))
            backward_time.append((t2 - t1))
            del graph_embeddings, target, batch, loss, e1, rel, e2
        print('Epoch {:04d} | Loss {:.4f} | Best MRR {:.4f} | Forward {:.4f}s | Backward {:.4f}s'.format(epoch, cum_loss, best_mrr, forward_time[(- 1)], backward_time[(- 1)]))
        if ((epoch % args.evaluate_every) == 0):
            if (use_cuda and (not args.no_cuda) and cpu_eval):
                model.cpu()
                test_graph.ndata['id'] = test_graph.ndata['id'].cpu()
                test_graph.ndata['norm'] = test_graph.ndata['norm'].cpu()
                test_graph.edata['type'] = test_graph.edata['type'].cpu()
                model.decoder.no_cuda = True
            model.eval()
            print('start eval')
            print('===========DEV============')
            mrr = evaluation_utils.ranking_and_hits(test_graph, model, valid_data, all_e1_to_multi_e2, train_network, fusion='graph-only', sim_relations=args.sim_relations, debug=args.debug, epoch=epoch)
            if (mrr < best_mrr):
                if (epoch >= args.n_epochs):
                    break
            else:
                best_mrr = mrr
                print('[saving best model so far]')
                torch.save({'state_dict': model.state_dict(), 'epoch': epoch}, model_state_file)
            metrics = {'best_mrr': best_mrr, 'cum_loss': cum_loss}
            with open(os.path.join(args.output_dir, 'metrics.json'), 'w') as f:
                f.write(json.dumps(metrics))
            if (use_cuda and (not args.no_cuda) and cpu_eval):
                model.cuda()
                test_graph.ndata['id'] = test_graph.ndata['id'].cuda()
                test_graph.ndata['norm'] = test_graph.ndata['norm'].cuda()
                test_graph.edata['type'] = test_graph.edata['type'].cuda()
                model.decoder.no_cuda = False
    print('training done')
    print('Mean forward time: {:4f}s'.format(np.mean(forward_time)))
    print('Mean Backward time: {:4f}s'.format(np.mean(backward_time)))
    print('\nStart testing')
    checkpoint = torch.load(model_state_file)
    model.eval()
    model.load_state_dict(checkpoint['state_dict'])
    print('Using best epoch: {}'.format(checkpoint['epoch']))
    evaluation_utils.ranking_and_hits(test_graph, model, test_data, all_e1_to_multi_e2, train_network, fusion='graph-only', sim_relations=args.sim_relations)
