import argparse
import sys
import os
import datetime

import utils.csv_exporter
import utils.myplotter
import utils.eps_plotter
from constants import *

def opt_parser():
    usage = 'Merge FL training results and plot figure from static freezing results and Gradually Freezing results.'
    parser = argparse.ArgumentParser(description=usage)
    parser.add_argument('--load_static_path', type=str, default='', help='Load Static Freeze results from path')
    parser.add_argument('--load_gf_path', type=str, default='', help='Load Gradually Freeze results from path')
    
    return parser.parse_args()


def get_static_freeze_data(filepath, pre_freeze_params):
    data = utils.csv_exporter.import_csv(filepath=filepath)


    # result_all_data = []
    # for row in data:
    #     transmission_volumes = eval(row['transmission_volume_history'])

    #     data['speedup_ratio'] = baseline_time / data['total_time']
    #     print(f'{data["speedup_ratio"]} {data["speedup_trans_ratio"]}')
        
    #     result_all_data.append(data)
    return data

def get_gradually_freeze_data_2(filepath, static_freeze_data):
    pretrained_acc = static_freeze_data[0]['acc'][:WARM_UP_ROUNDS]
    # print(pretrained_acc)
    
    data = utils.csv_exporter.import_csv(filepath=filepath)
    # print(data)
    new_data = []
    for row in data:
        gf_acc = [float(d)  for d in row['acc']]
        acc = pretrained_acc + gf_acc
        new_data.append(dict(name="Gradually Freezing: Primary Model", 
                                acc=acc, 
                                total_time=row['total_time'] , 
                                total_trainable_params=row['total_trainable_params'],
                                transmission_time=row['transmission_time'],
                                transmission_volume=row['transmission_volume'],
                                transmission_volume_readable=row['transmission_volume_readable'],
                                transmission_volume_history=row['transmission_volume_history']))
    # print(new_data)
    return new_data

def calc_speedup(all_data):
    baseline_time = 0
    for idx,  data in enumerate(all_data):
        if data.get('total_time'):
            pt = datetime.datetime.strptime(data['total_time'],'%H:%M:%S.%f')
            tt = pt - datetime.datetime(1900, 1, 1)
            total_seconds = tt.total_seconds()
            # print(total_seconds)
            data['total_time'] = total_seconds
            if 'Baseline' in data['name']:
                baseline_time = total_seconds
                print(baseline_time)
        if data.get('transmission_time'):
            pt = datetime.datetime.strptime(data['transmission_time'],'%H:%M:%S.%f') - datetime.datetime(1900, 1, 1)
            total_trans_seconds = pt.total_seconds()
            # print(total_trans_seconds)
            data['transmission_time'] = total_trans_seconds
            if 'Baseline' in data['name']:
                baseline_trans_time = total_trans_seconds
                # print(baseline_trans_time)
        print(f'Total time: {total_seconds} Total transmission time: {total_trans_seconds}')

    result_all_data = []
    for data in all_data:
        data['speedup_ratio'] = baseline_time / data['total_time']
        data['speedup_trans_ratio'] = baseline_trans_time / data['transmission_time']
        print(f'{data["speedup_ratio"]} {data["speedup_trans_ratio"]}')
        
        result_all_data.append(data)
    
    return result_all_data


def plot_epoch_to_accuracy(all_data, output_dir, timestamp, model_type):
    utils.eps_plotter.multiplot(
        all_data=all_data,
        y_label="Accuracy",
        title="",
        figure_idx=1
    )
    utils.eps_plotter.legend()
    utils.eps_plotter.save_figure(output_dir, f"{timestamp}_{model_type}_FL_epoch_to_Accuracy.eps")
    # utils.eps_plotter.save_figure(output_dir, f"{timestamp}_{model_type}_FL_epoch_to_Accuracy.png")



def plot_transmission_ratio(all_data, output_dir, model_type):
    utils.eps_plotter.plot_transmission_ratio(all_data=all_data, title=f'', figure_idx=3)
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_transmission_volume_reduction.eps')
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_transmission_volume_reduction.png') 



def plot_speedup(all_data, output_dir, model_type):
    utils.eps_plotter.plot_speedup_ratio(all_data, title=f'', figure_idx=4)
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_speedup.eps')
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_speedup.png') 



def plot_trans_to_acc(all_data, output_dir, model_type):
    utils.eps_plotter.plot_trans_to_acc(all_data, title=f'', figure_idx=5)
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_volume_to_acc.eps')
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_volume_to_acc.png') 

def plot_epoch_to_trans(all_data, output_dir, timestamp, model_type):
    pass
    utils.eps_plotter.plot_epoch_to_trans(
        all_data=all_data,
        y_label="Accuracy",
        title="",
        figure_idx=6
    )
    utils.eps_plotter.save_figure(output_dir, f"{timestamp}_{model_type}_FL_epoch_to_trans.eps")
    utils.eps_plotter.save_figure(output_dir, f"{timestamp}_{model_type}_FL_epoch_to_trans.png")
    utils.eps_plotter.block_show()


def plot_epoch_to_trans_new(all_data, output_dir, timestamp, model_type):
    prefreeze_volume = 0
    if model_type == 'ResNet-18':
        prefreeze_volume = (RESNET_18_PARAMS*4*8 * 5) /8/1024/1024  # 5: # of participant
    elif model_type == 'MobileNet':
        prefreeze_volume = (MOBILENET_PARAMS*4*8 * 5) /8/1024/1024 
    print(model_type, prefreeze_volume)
         
    
    utils.eps_plotter.plot_epoch_to_trans(
        all_data=all_data,
        prefreeze_volume=prefreeze_volume,
        title="",
        figure_idx=6
    )
    utils.eps_plotter.save_figure(output_dir, f"{timestamp}_{model_type}_s1_FL_epoch_to_trans.eps")
    utils.eps_plotter.save_figure(output_dir, f"{timestamp}_{model_type}_s1_FL_epoch_to_trans.png")
    utils.eps_plotter.block_show()


def plot_trans_to_target_acc(all_data, output_dir, model_type):
    utils.eps_plotter.plot_trans_to_target_acc(all_data, title=f'', figure_idx=10, model_type=model_type)
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_volume_to_target_acc.eps')
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_volume_to_target_acc.png')
    utils.eps_plotter.block_show()


def plot_duration(all_data, output_dir, model_type):
    utils.eps_plotter.plot_duration(all_data=all_data, title=f'', figure_idx=12)
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_duration.eps')
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_duration.png') 

def plot_volume(all_data, output_dir, model_type):
    utils.eps_plotter.plot_volume(all_data=all_data, title=f'', figure_idx=13)
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_trans_volume.eps')
    utils.eps_plotter.save_figure(base_dir=output_dir, filename=f'{model_type}_trans_volume.png') 


if __name__ == '__main__':
    cmd_args = opt_parser()
    if not cmd_args.load_static_path or not cmd_args.load_gf_path:
        print('PATH ERROR')
        sys.exit(0)
    
    if 'resnet' in cmd_args.load_static_path:
        model_type = 'ResNet-18'
        pre_freeze_params = RESNET_18_PARAMS
    elif 'mobilenet' in cmd_args.load_static_path:
        model_type = 'MobileNet'
        pre_freeze_params = MOBILENET_PARAMS
    else:
        model_type = 'LeNet-5'
        pre_freeze_params = LENET_5_PARAMS


    static_data = get_static_freeze_data(cmd_args.load_static_path, pre_freeze_params)
    gf_data = get_gradually_freeze_data_2(cmd_args.load_gf_path, static_data)
    all_data = static_data + gf_data
    new_all_data = calc_speedup(all_data)
    print(len(all_data))

    # Create output folder
    script_time = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_dir = f'./03-FL/resnet-result/s1_{script_time}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    print(new_all_data[0].keys())
    merged_csv_filename = os.path.join(output_dir, f'{script_time}__merged.csv')
    print(merged_csv_filename)
    utils.csv_exporter.export_csv(data=new_all_data, filepath=merged_csv_filename, fields=new_all_data[1].keys())

    plot_epoch_to_accuracy(all_data=new_all_data, output_dir=output_dir, timestamp=script_time, model_type=model_type)


    print(os.path.abspath(merged_csv_filename))
