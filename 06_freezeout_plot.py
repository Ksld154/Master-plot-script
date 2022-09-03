import datetime
import os
import time

import tools.csv_exporter as csv_exporter
import tools.new_plotter as new_plotter

## new lenet e=50
OURS_CSV = './06-freezeout/ours_result.csv'
NOSWITCH_CSV = './06-freezeout/no-switch-result.csv'


def setup_folders(model_type):
    base_dir = os.path.dirname(__file__)
    now = datetime.datetime.now()
    dt_string = now.strftime("%m-%d-%Y_%H%M%S")
    results_dir = os.path.join(base_dir, './06-freezeout/result', f'{dt_string}_{model_type}')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    print(results_dir)
    
    return results_dir



def plot_acc(output_dir=None, model_type=None):
    csv_file_1 = OURS_CSV
    csv_file_2 = NOSWITCH_CSV
    
    # raw_data = []
    csv1_raw_data = csv_exporter.import_csv(filepath=csv_file_1)
    # print(csv1_raw_data)
    new_plotter.plot_acc(all_data=csv1_raw_data, figure_idx=1)
    # new_plotter.save_figure(os.path.join(output_dir, f'{model_type}_ours_acc.png')) 
    new_plotter.save_figure(os.path.join(output_dir, f'{model_type}_ours_acc.eps')) 
    
    csv2_raw_data = csv_exporter.import_csv(filepath=csv_file_2)
    new_plotter.plot_acc(all_data=csv2_raw_data, figure_idx=2)
    # new_plotter.save_figure(os.path.join(output_dir, f'{model_type}_no_switch_acc.png')) 
    new_plotter.save_figure(os.path.join(output_dir, f'{model_type}_no_switch_acc.eps')) 



if __name__ == '__main__':
    

    model_type = 'lenet'
    output_dir = setup_folders(model_type=model_type)

    # plot_best_acc(output_dir=output_dir, model_type=model_type)
    # time.sleep(1)
    
    plot_acc(output_dir=output_dir, model_type=model_type)
    time.sleep(1)

    # new_plotter.show()