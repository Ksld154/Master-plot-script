import datetime
import os
import time

import tools.csv_exporter as csv_exporter
import tools.new_plotter as new_plotter


## new mobilenet e=100
RESULT_CSV_1 = './02-single_model/mobilenet/results_mobilenet_e=100_pre=0.1_window=5_staticTrue_gfTrue.csv'
RESULT_CSV_2 = './02-single_model/mobilenet/results_mobilenet_e=100_pre=0.25_window=5_staticTrue_gfTrue.csv'
METRIC_CSV_1 = './02-single_model/mobilenet/metrics_mobilenet_e=100_pre=0.1_window=5_staticTrue_gfTrue.csv'
METRIC_CSV_2 = './02-single_model/mobilenet/metrics_mobilenet_e=100_pre=0.25_window=5_staticTrue_gfTrue.csv'


def setup_folders(model_type):
    base_dir = os.path.dirname(__file__)
    now = datetime.datetime.now()
    dt_string = now.strftime("%m-%d-%Y_%H%M%S")
    results_dir = os.path.join(base_dir, './02-single_model/mobilenet-result', f'{dt_string}_{model_type}')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    print(results_dir)
    return results_dir

def plot_best_acc(output_dir=None, model_type=None):
    csv_file_1 = RESULT_CSV_1
    csv_file_2 = RESULT_CSV_2
    
    all_data = []
    all_data.append(csv_exporter.import_csv(filepath=csv_file_1))
    all_data.append(csv_exporter.import_csv(filepath=csv_file_2))
    # model_type = 'resnet' if 'resnet' in csv_file_1 else 'mobilenet'
    # model_type = 'mobilenet' if 'mobilenet' in csv_file_1 else 'lenet'

    new_plotter.plot_best_acc(all_data=all_data, title=f'Best Accuracy w.r.t.Initial Freezing Point (Model: {model_type})', figure_idx=2)
    new_plotter.save_figure(os.path.join(output_dir, f'{model_type}_best_acc.eps'))  


def plot_acc(output_dir=None, model_type=None):
    csv_file_1 = RESULT_CSV_1
    csv_file_2 = RESULT_CSV_2
    
    # raw_data = []
    csv1_raw_data = csv_exporter.import_csv(filepath=csv_file_1)
    # print(csv1_raw_data)
    new_plotter.plot_acc(all_data=csv1_raw_data, figure_idx=4)
    new_plotter.save_figure(os.path.join(output_dir, f'{model_type}_pre0.1_acc.eps')) 
    
    csv2_raw_data = csv_exporter.import_csv(filepath=csv_file_2)
    new_plotter.plot_acc(all_data=csv2_raw_data, figure_idx=5)
    new_plotter.save_figure(os.path.join(output_dir, f'{model_type}_pre0.25_acc.eps')) 

def plot_total_training_time(output_dir=None, model_type=None):
    csv_file_1 = METRIC_CSV_1
    csv_file_2 = METRIC_CSV_2
    
    raw_data = []
    raw_data.append(csv_exporter.import_csv(filepath=csv_file_1))
    raw_data.append(csv_exporter.import_csv(filepath=csv_file_2))
    
    new_all_data = []
    for data in raw_data:
        new_all_data.append(new_plotter.calc_transmission_speedup(all_data=data))
    print(new_all_data)

    new_plotter.plot_training_time(all_data=new_all_data,  figure_idx=10, model_type=model_type)
    new_plotter.save_figure(os.path.join(output_dir, f'{model_type}_total_training_time.eps')) 


def plot_total_trainable_params(output_dir=None, model_type=None):
    csv_file_1 = METRIC_CSV_1
    csv_file_2 = METRIC_CSV_2
    
    raw_data = []
    raw_data.append(csv_exporter.import_csv(filepath=csv_file_1))
    raw_data.append(csv_exporter.import_csv(filepath=csv_file_2))

    new_plotter.plot_transmission_volume(all_data=raw_data,  figure_idx=11, model_type=model_type)
    new_plotter.save_figure(os.path.join(output_dir, f'{model_type}_total_trainable_params.eps')) 
    new_plotter.block_show()


if __name__ == '__main__':
    
    if 'resnet' in RESULT_CSV_1:
        model_type = 'resnet'
    elif 'mobilenet' in RESULT_CSV_1:
        model_type = 'mobilenet'
    else:
        model_type = 'lenet'
    output_dir = setup_folders(model_type=model_type)

    # plot_best_acc(output_dir=output_dir, model_type=model_type)
    # time.sleep(1)
    
    plot_acc(output_dir=output_dir, model_type=model_type)
    time.sleep(1)
    
    plot_total_training_time(output_dir=output_dir, model_type=model_type)
    time.sleep(1)
    plot_total_trainable_params(output_dir=output_dir, model_type=model_type)
    time.sleep(1)

    # new_plotter.show()