import os
import numpy as np
import pandas as pd
from datetime import datetime, date
from utils import *
import matplotlib.pyplot as plt



def type1(df, label_idx, number, refresh_rate, bitrate, SAVE = False):
    """x axis is bandwidth, y axis is JOD, color is resolution"""
    bitrate_df = df.iloc[label_idx, 0] # check if bitrate is correct
    if DEBUG:
        print(f'bitrate_df {bitrate_df}, bitrate {bitrate}')

    assert bitrate_df == bitrate

    # fig, ax = plt.subplots(figsize=(8, 5))
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

def type2(df, label_idx, bitrate, number, refresh_rate, SAVE = False):
    """x axis is resolution, y axis is JOD, color is bitrate, labels are refresh rate"""
    bitrate_df = df.iloc[label_idx, 0] # check if bitrate is correct
    if DEBUG:
        print(f'bitrate_df {bitrate_df}, bitrate {bitrate}')

    x_values = np.array([1080, 864, 720, 480, 360,]) # resolution
    x_values = sorted(x_values)
    # print(f'\n\n\n')
    # fig, ax = plt.subplots(figsize=(8, 5))
    for num in range(number): # loop column
        # cvvdp jod from file1
        jod_cvvdp = df.iloc[label_idx, 1+5*num:6+5*num].values
        jod_cvvdp = [float(v) for v in jod_cvvdp]        

        # print(f'idx {num}, fps{refresh_rate[num]}, JOD {jod_cvvdp}, ') # max JOD {max(jod_cvvdp)}
        max_jod_idx = np.argmax(jod_cvvdp)
        # print(f'idx {num}, fps{refresh_rate[num]}, JOD {jod_cvvdp}, max JOD {max(jod_cvvdp)}')
        max_jod.append(max(jod_cvvdp))
        max_res.append(x_values[max_jod_idx])


def plot_by_velocity(max_comb_per_bitrate):
    """
    max_comb_per_bitrate: e.g. for bitrate 500kbps, key:val -> path_seg: best combination of velocity
    {path2_seg3': [[40, 720], [80, 720], [110, 480]], 'path3_seg1': [[90, 720], [80, 480], [120, 480]],}
    
    """
    resolutions = [360, 480, 720, 864, 1080]
    # colors = ['blue', 'greenyellow', 'red', 'green', 'orange',]
    # colors = ['blue', 'greenyellow', 'red', 'gray', 'cyan', 'green', 'orange',]

    marker_sizes = [15, 55, 105]

    plt.figure(figsize=(10, 6))
    count = 0
    for key, value in max_comb_per_bitrate.items():
        # Extract framerates and resolutions from the value
        frs, ress = zip(*value)
        print(f'frs, ress {frs, ress}')
        plt.scatter(ress, frs, s=marker_sizes, label=key, marker='o', color=colors_matplotlib[count]) 
        plt.plot(ress, frs, color=colors_matplotlib[count], linestyle='-', linewidth=2)  # Line connecting the points
        count += 1

    plt.xticks(resolutions)
    plt.yticks(refresh_rate)
    plt.title('Framerate vs Resolution for Different Paths')
    plt.legend()
    plt.grid(True)
    plt.show()
            


# to analyze velocity
if __name__ == "__main__":
    SAVE = False # False, False
    SHOW = False
    DEBUG = False

    VRR_PLOT_HPC = r'C:\Users\15142\Projects\VRR\VRR_Plot_HPC'
    
    # bitrates = [400, 700, 900]
    # bitrates = [300,]
    # bitrates = [500, 1000, 1500, 2000]
    bitrates = [500,]
    bitrate_dict = {bitrate: index for index, bitrate in enumerate(bitrates)}
    print(bitrate_dict)
    
    SCENES = ['bedroom', 'bistro', 'crytek_sponza', 'gallery', 'living_room', 'lost_empire', 'room', 'sibenik', 'suntemple', 'suntemple_statue']
    # SCENES = ['bedroom', 'crytek_sponza', 'gallery', 'living_room', 'lost_empire', 'room', 'sibenik', 'suntemple', 'suntemple_statue']
    SCENES = ['bistro']
    excel_date = '500_1500_2000kbps' # '400_700_900kbps'
    
    for scene_name in SCENES:
        print(f'\n\n\n================================== SCENE {scene_name} ==================================')
        file_path = f'{VRR_PLOT_HPC}/data-{excel_date}/{scene_name}.xlsx'
        for bitrate in bitrates:
            print(f'=============================== bitrate {bitrate} ===============================')
            max_comb_per_bitrate = {} # { path1_seg1: [[fps1, res1], [fps2, res2], [fps3, res3]] }
            for path in range(1, 5):
                for seg in range(1, 4):
                    sequence_name = f'path{path}_seg{seg}'
                    max_comb_per_bitrate[sequence_name] = []
                    # print(f'max_comb_per_bitrate {max_comb_per_bitrate}')
                    for speed in range(1, 4):
                        if SAVE:
                            today = date.today()
                            scene_output_dir = f'{VRR_PLOT_HPC}/plot-{today}/{scene_name}'
                            os.makedirs(scene_output_dir, exist_ok=True)

                        sheet_name = f'path{path}_seg{seg}_{speed}'
                        df = pd.read_excel(file_path, sheet_name=sheet_name, na_values=['NA'])
                        # print(f'================== sheet_name {sheet_name} =================')
                        # for bitrate in bitrates:
                        max_jod, max_res = [], []
                        type1(df, bitrate_dict[bitrate], len(refresh_rate), refresh_rate, bitrate, SAVE)
                        type2(df, bitrate_dict[bitrate], bitrate, len(refresh_rate), refresh_rate, SAVE)
                        # print(f'max_jod {max_jod}')
                        max_idx = np.argmax(max_jod) # only availble if type2 is run
                        # print(f'\nmax_res {max_res}')
                        # print(f'bitrate {bitrate}, max JOD is {max_jod[max_idx]} with resolution {max_res[max_idx]} fps {refresh_rate[max_idx]}\n')
                        max_comb_per_bitrate[sequence_name].append([refresh_rate[max_idx], max_res[max_idx]])
                        # print(f'max_comb_per_bitrate {max_comb_per_bitrate}')
            print(f'{bitrate}kbps {max_comb_per_bitrate}')

            plot_by_velocity(max_comb_per_bitrate)