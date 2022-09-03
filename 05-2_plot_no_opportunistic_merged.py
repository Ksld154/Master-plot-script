import os
import datetime

from matplotlib.pyplot import plot

import utils.csv_exporter
import utils.myplotter
import utils.no_opportunistic_plotter
from constants import *




def plot_trans_to_target_acc_new(all_data, output_dir):
    utils.no_opportunistic_plotter.plot_trans_to_target_acc(all_data=all_data, figure_idx=19, model_type='merged', title='')
    utils.no_opportunistic_plotter.save_figure(base_dir=output_dir, filename=f'merged_transmission_volume_to_target_acc.eps')
    # utils.no_opportunistic_plotter.save_figure(base_dir=output_dir, filename=f'merged_transmission_volume_to_target_acc.png')


def plot_accuracy_to_transmission_volume_ratio(all_data):
    # 1. get best acc
    resnet_data = all_data[0]
    mobilenet_data = all_data[1]

    resnet_best_accs = [max(model['acc']) for model in resnet_data]
    mobilenet_best_accs = [max(model['acc']) for model in mobilenet_data]
    all_best_accs = [resnet_best_accs, mobilenet_best_accs]
    print(all_best_accs)
    
    # 2. get total_transmission volume
    resnet_transmission_volume = [float(model['transmission_volume'])/8/1024/1024/1024 for model in resnet_data]
    mobilenet_transmission_volume = [float(model['transmission_volume'])/8/1024/1024/1024 for model in mobilenet_data]
    all_transmission_volume = [resnet_transmission_volume, mobilenet_transmission_volume]
    print(all_transmission_volume)

    # 3. calculate the ratio
    resnet_accuracy_to_transmission_volume_ratio = [ x/y for _, (x, y) in enumerate(zip(resnet_best_accs, resnet_transmission_volume)) ]
    mobilenet_accuracy_to_transmission_volume_ratio = [ x/y for _, (x, y) in enumerate(zip(mobilenet_best_accs, mobilenet_transmission_volume)) ]
    all_ratio = [resnet_accuracy_to_transmission_volume_ratio, mobilenet_accuracy_to_transmission_volume_ratio]
    print(all_ratio)

    # 4. plot
    model_name = [model['name'] for model in resnet_data]
    utils.no_opportunistic_plotter.plot_accuracy_to_transmission_volume_ratio(
        all_data=all_ratio, 
        figure_idx=15, 
        model_name=model_name)
    utils.no_opportunistic_plotter.save_figure(base_dir='.', filename=f'merged_accuracy_to_transmission_volume_ratio.eps')
    utils.no_opportunistic_plotter.save_figure(base_dir='.', filename=f'merged_accuracy_to_transmission_volume_ratio.png')
    # utils.no_opportunistic_plotter.block_show()

def plot_epoch_to_target_acc(all_data, output_dir):
    utils.no_opportunistic_plotter.plot_epoch_to_target_acc(all_data=all_data, figure_idx=20, model_type='merged', title='')
    utils.no_opportunistic_plotter.save_figure(base_dir=output_dir, filename=f'merged_epoch_to_target_acc.eps')
    # utils.no_opportunistic_plotter.save_figure(base_dir=output_dir, filename=f'merged_epoch_to_target_acc.png')


if __name__ == '__main__':    

    # merge 2 kinds of model on the same graph
    resnet_data = utils.csv_exporter.import_csv(filepath='./05-nonopp/resnet_no_opportunistic_switch_2.csv')
    mobilenet_data = utils.csv_exporter.import_csv(filepath='./05-nonopp/mobilenet_no_opportunistic_switch.csv')
    # plot_accuracy_to_transmission_volume_ratio(
    #     all_data=[resnet_data, mobilenet_data] 
    # )

    
    merged_data = utils.csv_exporter.import_csv(filepath='./05-nonopp/merged_no-opp_switch.csv')
    plot_trans_to_target_acc_new(all_data=merged_data, output_dir='./05-nonopp')
    plot_epoch_to_target_acc(all_data=merged_data, output_dir='./05-nonopp')
