# Script Command

## Prerequisite

```bash
git clone git@github.com:Ksld154/Master-plot-script.git
conda create --name "plot-eps" --file requirements.txt
# conda create --name plot-eps python=3.10
# conda activate plot-eps
# conda install numpy matplotlib pandas
```

## 5-2 Single Model

```bash
## lenet (fig. 5.1 + 5.4 + 5.5)
python 02_lenet_plotter.py

## mobilenet (fig. 5.2 + 5.4 + 5.5)
python 02_mobilenet_plotter.py

## resnet (fig. 5.3 + 5.4 + 5.5)
python 02_resnet_plotter.py
```

## 5-3 FL

```bash
## lenet
python 03_lenet-merge_plot.py --load_static_path "./03-FL/lenet_e=100_window=5_static_result.csv" --load_gf_path "./03-FL/result.csv"

## resnet (fig. 5.6 + 5.10 + 5.11)
python 03_resnet-merge_plot.py \
--load_static_path "./03-FL/resnet/resnet_e=100_window=5_static_result.csv" \
--load_gf_path "./03-FL/resnet/result.csv"

## resnet (fig. 5.7)
python 03_resnet-s1_merge_plot.py \
--load_static_path "./03-FL/resnet/s1/resnet_e=100_window=5_static_result.csv" \
--load_gf_path "./03-FL/resnet/s1/result.csv"

## resnet (fig. 5.8 + 5.9)
python 03_resnet-plot_trans_duration.py \
--load_group1 "./03-FL/resnet/resnet_iidTrue_num10_C0.5_le1__static=2022-06-05_112426__gf=2022-06-12_170103__merged.csv" \
--load_group2 "./03-FL/resnet/resnet_iidTrue_num10_C1.0_le1__static=2022-06-05_112424__gf=2022-06-22_103249__merged.csv"

## mobilenet (fig. 5.6 + 5.10 + 5.11)
python 03_mobilenet-merge_plot.py \
--load_static_path "./03-FL/mobilenet/mobilenet_e=100_window=5_static_result.csv" \
--load_gf_path "./03-FL/mobilenet/result.csv"

## mobilenet (fig. 5.7)
python 03_mobilenet-s1_merge_plot.py \
--load_static_path "./03-FL/mobilenet/s1/mobilenet_e=100_window=5_static_result.csv" \
--load_gf_path "./03-FL/mobilenet/s1/result.csv"

## mobilenet (fig. 5.8 + 5.9)
python 03_mobilenet-plot_trans_duration.py \
--load_group1 "./03-FL/mobilenet/mobilenet_iidTrue_num10_C0.5_le1__static=2022-06-05_112433__gf=2022-06-12_215753__merged.csv" \
--load_group2 "./03-FL/mobilenet/mobilenet_iidTrue_num10_C1.0_le1__static=2022-06-05_112427__gf=2022-06-22_103432__merged.csv"

```

## 5-4-1 Non-IID

```bash
## resnet
python 04-1_plot-noniid.py \
--load_static_path "./04-1-noniid/resnet/resnet_e=100_window=5_static_result.csv" \
--load_gf_path "./04-1-noniid/resnet/result.csv"

## mobilenet
python 04-1_plot-noniid.py \
--load_static_path "./04-1-noniid/mobilenet/mobilenet_e=100_window=5_static_result.csv" \
--load_gf_path "./04-1-noniid/mobilenet/result.csv"
```

## 5-4-2 Sync Freq

```bash
python 04-2_plot-diff-freq-group.py --load_file "./04-2-syncfreq/diff_freq_resnet2.csv"
python 04-2_plot-diff-freq-group.py --load_file "./04-2-syncfreq/diff_freq_mobilenet2.csv"
```

## 5-5 Non Opp.

```bash
## [Note] To drag the legend to appropriate locations, please execute the script on your local computer
## if you want to execute it on remote server, please run it through MobaXterm (for enabling X11 server)

## mobile & resnet
python 05-1_mobilenet_plot_no_opportunistic.py
python 05-1_resnet_plot_no_opportunistic.py

## merged figure
python 05-2_plot_no_opportunistic_merged.py
```

## 5-6 FreezeOut

```bash
## test
python 06_freezeout_plot.py
```
