import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt



def type1(df, label_idx, number, refresh_rate, bitrate, SAVE = False):
    """x axis is bandwidth, y axis is JOD, color is resolution"""
    # bandwidth_dict = {10.37349118: 32000, 9.680344: 16000, 8.98719682:8000}
    fig, ax = plt.subplots(figsize=(8, 5))

    labels = ['360p', '480p', '720p', '864p', '1080p']
    colors = ['blue', 'greenyellow', 'red', 'green', 'orange',]
    # colors = ['blue', 'greenyellow', 'red', 'gray', 'cyan', 'green', 'orange',]

    # collect data for each resolution
    # manually skip the resolution we dont want
    resolution_not_want = ['540p']
    for i, resolution in enumerate(labels):
        # print(f'\n\n\ni resolution {i, resolution}')
        if resolution in resolution_not_want:
            continue

        jod = []
        for num in range(0, number): # e.g. first 3 fps, i.e. 30, 60, 70
            val = df.iloc[label_idx, 1+i+5*num]
            jod.append(val)
        jod = [float(v) for v in jod]        
        # print(f'resolution {resolution}, jod {jod}, label {labels[i]}')
        ax.plot(refresh_rate, jod, marker='o', label=labels[i], linestyle='-', color=colors[i])

    ax.set_xlabel('Refresh rate (Hz)')
    ax.set_xticks(refresh_rate)
    ax.set_ylabel('JOD')
    ax.set_title(f'CVVDP results- path{path}_seg{seg}, speed {speed} - {bitrate} kbps')
    ax.grid(True)
    ax.legend()

    if SAVE:
        date = datetime.now().strftime("%m-%d")
        output_dir = os.path.join(f'{VRR_PLOT_HPC}/plot-{date}/', f'{scene_name}_plot1_{sheet_name}')        
        os.makedirs(output_dir, exist_ok=True)
        # current_time = datetime.now().strftime("%H%M")
        plt.savefig(f"{output_dir}/p1_{sheet_name}_{bitrate}.png")

    if SHOW:
        plt.show()


def type2(df, label_idx, bitrate, number, refresh_rate, SAVE = False):
    """x axis is resolution, y axis is JOD, color is bitrate, labels are refresh rate"""
    x_values = np.array([1080, 864, 720, 480, 360,]) # resolution
    x_values = sorted(x_values)
    # print(f'\n\n\n')
    fig, ax = plt.subplots(figsize=(8, 5))
    for num in range(number): # loop column
        # cvvdp jod from file1
        jod_cvvdp = df.iloc[label_idx, 1+5*num:6+5*num].values
        jod_cvvdp = [float(v) for v in jod_cvvdp]        

        # print(f'idx {num}, fps{refresh_rate[num]}, JOD {jod_cvvdp}, ') # max JOD {max(jod_cvvdp)}
        max_jod_idx = np.argmax(jod_cvvdp)
        # print(f'idx {num}, fps{refresh_rate[num]}, JOD {jod_cvvdp}, max JOD {max(jod_cvvdp)}')
        max_jod.append(max(jod_cvvdp))
        max_res.append(x_values[max_jod_idx])

        ax.plot(x_values, jod_cvvdp, marker='o', label=f'{refresh_rate[num]} fps')
        ax.set_xticks(x_values)

    ax.set_xlabel('Resolution')
    ax.set_ylabel('JOD')
    ax.set_title(f'CVVDP results - path{path}_seg{seg}, speed {speed} - {bitrate} kbps')
    ax.grid(True)
    ax.legend()
    if SAVE:
        date = datetime.now().strftime("%m-%d")
        output_dir = os.path.join(f'{VRR_PLOT_HPC}/plot-{date}/', f'{scene_name}_plot2_{sheet_name}')
        os.makedirs(output_dir, exist_ok=True)
        # current_time = datetime.now().strftime("%H%M")
        fig.savefig(f"{output_dir}/p2_{sheet_name}_{bitrate}.png")
    if SHOW:
        plt.show()



# download cvvdp results from HPC
# process results by running this file
# write to excel using write_excel.py
# plot using plot_cvvdp.py

# suitable for excel written using program, e.g. suntemple-05-03, sheetname fast, with 30-120fps
# Plot cvvdp results from csv file
# in type 2 change 2+6*num:9+6*num to 2+7*num:9+7*num if has 676 column
if __name__ == "__main__":
    SAVE = True # True, False
    SHOW = True

    VRR_PLOT_HPC = r'C:\Users\15142\Projects\VRR\VRR_Plot_HPC'
    scene_name = 'bistro' # suntemple_statue
    file_path = f'{VRR_PLOT_HPC}/data-08-09/{scene_name}.xlsx'

    bitrate_dict = {500: 0, 1000: 1, 1500: 2, 2000: 3,}
    refresh_rate = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    bitrates = [500, 1000, 1500, 2000]
    bitrates = [500,]

    for path in range(1, 6):
        for seg in range(1, 4):
            for speed in range(1, 4):
                sheet_name = f'path{path}_seg{seg}_{speed}'
                df = pd.read_excel(file_path, sheet_name=sheet_name, na_values=['NA'])
                print(f'SCENE {sheet_name}')
                for bitrate in bitrates:
                    print(f'bitrate {bitrate}')
                    print(f'\n\n\n================= bitrate {bitrate} =================')
                    max_jod = []
                    max_res = []
                    type1(df, bitrate_dict[bitrate], len(refresh_rate), refresh_rate, bitrate, SAVE)
                    type2(df, bitrate_dict[bitrate], bitrate, len(refresh_rate), refresh_rate, SAVE)
                    print(f'max_jod {max_jod}')
                    max_idx = np.argmax(max_jod) # only availble if type2 is run
                    # print(f'\nmax_res {max_res}')
                    print(f'bitrate {bitrate}, max JOD is {max_jod[max_idx]} with resolution \
                        {max_res[max_idx]} fps {refresh_rate[max_idx]}')
