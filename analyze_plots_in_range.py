import os
import random
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
        # max_idx = np.argmax(max_jod) # only availble if type2 is run
        # print(f'bitrate {bitrate}, max JOD is {max_jod[max_idx]} with resolution {max_res[max_idx]} fps {refresh_rate[max_idx]}')
        # max_comb_per_sequence[sheet_name].append([refresh_rate[max_idx], max_res[max_idx]])


def find_comb_within_range(df, label_idx, bitrate, max_comb_per_sheet):
    """
    res, fps whose jod is within range of the biggest of the sheet
    max_comb_per_sheet for path1_seg2_3 is like [[80, 480, 7.1158], [120, 720, 7.5596], [120, 720, 7.7879], [120, 720, 7.9228]]
    """
    # bitrate_df = df.iloc[label_idx, 0] # check if bitrate is correct
    comb_within_range_per_sheet = []


    for num in range(len(refresh_rate)): # loop column
        # cvvdp jod from file1
        jod_cvvdp = df.iloc[label_idx, 1+5*num:6+5*num].values
        jod_cvvdp = [float(v) for v in jod_cvvdp] 
        
        # Find values within THRESHOLD 0.25 range of the maximum
        max_jod_val_per_bitrate = max_comb_per_sheet[label_idx][2]

        close_to_max = [(index, value) for index, value in enumerate(jod_cvvdp) if abs(max_jod_val_per_bitrate - value) <= THRESHOLD]
        # print(f"\nBitrate {bitrate}, Maximum JOD: {max_jod_val_per_bitrate}")
        if len(close_to_max) == 0:
            continue  
        # print("jod_cvvdp:", jod_cvvdp)   
        # print("Values within 0.25 range of the maximum:", close_to_max)   
        for index, jod in close_to_max:
            # print(f'jod, refresh_rate, resolution {jod, refresh_rate[num], x_values[index]}')
            comb_within_range_per_sheet.append((refresh_rate[num], x_values[index]))
    # print(f'comb_within_range_per_sheet {comb_within_range_per_sheet}')
    return comb_within_range_per_sheet
        # 7.7625 fps 90 720p


# find all refresh rate and resolution within range of 0.25 of the max jod
# get values like crytek_sponza_max_comb_per_sequence = {'path1_seg1_1': [[60, 720], [70, 1080], [80, 1080], [80, 1080]], 'path1_seg1_2': [[90, 480], [120, 720], [120, 720], [120, 720]], 'path1_seg1_3': [[100, 480], [120, 720], [120, 720], [120, 720]], 'path1_seg2_1': [[50, 720], [40, 1080], [50, 1080], [60, 1080]], 'path1_seg2_2': [[80, 720], [90, 720], [110, 720], [110, 720]], 'path1_seg2_3': [[80, 480], [120, 720], [120, 720], [120, 720]], 'path1_seg3_1': [[50, 720], [40, 1080], [50, 1080], [50, 1080]], 'path1_seg3_2': [[80, 720], [80, 720], [110, 720], [110, 720]], 'path1_seg3_3': [[90, 720], [110, 720], [120, 720], [120, 720]], 'path2_seg1_1': [[30, 720], [40, 1080], [40, 1080], [50, 1080]], 'path2_seg1_2': [[80, 720], [80, 720], [90, 720], [90, 720]], 'path2_seg1_3': [[80, 480], [90, 720], [120, 720], [120, 720]], 'path2_seg2_1': [[30, 720], [40, 1080], [40, 1080], [40, 1080]], 'path2_seg2_2': [[60, 720], [70, 720], [80, 720], [80, 720]], 'path2_seg2_3': [[70, 720], [80, 720], [90, 720], [90, 720]], 'path2_seg3_1': [[40, 720], [50, 720], [60, 720], [50, 1080]], 'path2_seg3_2': [[80, 720], [80, 720], [90, 720], [110, 720]], 'path2_seg3_3': [[80, 480], [110, 720], [120, 720], [120, 720]], 'path3_seg1_1': [[30, 720], [50, 720], [60, 720], [60, 720]], 'path3_seg1_2': [[80, 720], [80, 720], [90, 720], [110, 720]], 'path3_seg1_3': [[80, 720], [100, 720], [110, 720], [120, 720]], 'path3_seg2_1': [[40, 720], [50, 720], [60, 720], [50, 1080]], 'path3_seg2_2': [[60, 720], [70, 720], [80, 720], [80, 720]], 'path3_seg2_3': [[80, 720], [90, 720], [90, 720], [110, 720]], 'path3_seg3_1': [[40, 720], [60, 720], [70, 720], [50, 1080]], 'path3_seg3_2': [[60, 720], [70, 720], [80, 720], [110, 720]], 'path3_seg3_3': [[70, 720], [80, 720], [90, 720], [110, 720]], 'path4_seg1_1': [[30, 720], [30, 1080], [30, 1080], [30, 1080]], 'path4_seg1_2': [[40, 720], [50, 720], [40, 1080], [50, 1080]], 'path4_seg1_3': [[50, 720], [50, 720], [60, 720], [60, 720]], 'path4_seg2_1': [[30, 720], [40, 720], [30, 1080], [30, 1080]], 'path4_seg2_2': [[30, 720], [50, 720], [50, 720], [40, 1080]], 'path4_seg2_3': [[40, 720], [50, 720], [60, 720], [70, 720]], 'path4_seg3_1': [[30, 720], [30, 1080], [30, 1080], [30, 1080]], 'path4_seg3_2': [[40, 720], [50, 720], [40, 1080], [50, 1080]], 'path4_seg3_3': [[40, 720], [60, 720], [50, 1080], [60, 1080]], 'path5_seg1_1': [[30, 720], [40, 1080], [40, 1080], [50, 1080]], 'path5_seg1_2': [[60, 720], [80, 720], [90, 720], [100, 720]], 'path5_seg1_3': [[80, 720], [90, 720], [110, 720], [110, 720]], 'path5_seg2_1': [[50, 720], [60, 720], [70, 720], [60, 1080]], 'path5_seg2_2': [[80, 480], [90, 720], [110, 720], [110, 720]], 'path5_seg2_3': [[80, 480], [90, 720], [120, 720], [120, 720]], 'path5_seg3_1': [[60, 720], [80, 720], [90, 720], [90, 720]], 'path5_seg3_2': [[110, 480], [120, 720], [120, 720], [120, 720]], 'path5_seg3_3': [[110, 480], [110, 480], [120, 720], [120, 720]]}
# next step, process_drop_jod.py in Scatter_Plot_App
if __name__ == "__main__":
    SAVE = True # True, False
    SHOW = False
    DEBUG = False
    WRITE_DICT = True
    THRESHOLD = 0.6 # TODO: change threshold

    VRR_PLOT_HPC = r'C:\Users\15142\Projects\VRR\Data\VRR_Plot_HPC'
    
    bitrates = [500, 1000, 1500, 2000]
    # bitrates = [500,]
    
    bitrate_dict = {bitrate: index for index, bitrate in enumerate(bitrates)}
    print(f'bitrate_dict {bitrate_dict}')
    x_values = np.array([1080, 864, 720, 480, 360,]) # resolution
    x_values = sorted(x_values)
    
    SCENES = ['bedroom', 'bistro', 'crytek_sponza', 'gallery', 'living_room', 'lost_empire', 'room', 'sibenik', 'suntemple', 'suntemple_statue']
    # SCENES = ['crytek_sponza','bistro']
    excel_date = '500_1500_2000kbps' # '400_700_900kbps'

    if WRITE_DICT:
        now = datetime.now()
        time_path = now.strftime("%Y-%m-%d-%H_%M")
    for scene_name in SCENES:
        print(f'\n\n\n================================== SCENE {scene_name} ==================================')
        file_path = f'{VRR_PLOT_HPC}/data-{excel_date}/{scene_name}.xlsx'
        max_comb_per_sequence = {} 
        comb_within_range_per_sequence = {} 

        for bitrate in bitrates:
            print(f'=============================== bitrate {bitrate} ===============================')
            max_comb_per_bitrate = {} # { path1_seg1: [[fps1, res1], [fps2, res2], [fps3, res3]] }
            for path in range(1, 6):
                for seg in range(1, 4):
                    sequence_name = f'path{path}_seg{seg}'
                    max_comb_per_bitrate[sequence_name] = []
                    # print(f'max_comb_per_bitrate {max_comb_per_bitrate}')
                    for speed in range(1, 4):
                        if SAVE:
                            today = date.today()
                            scene_output_dir = f'{VRR_PLOT_HPC}/analysis-{today}/{scene_name}'
                            os.makedirs(scene_output_dir, exist_ok=True)

                        sheet_name = f'path{path}_seg{seg}_{speed}'
                        max_comb_per_sequence.setdefault(sheet_name, [])
                        comb_within_range_per_sequence.setdefault(sheet_name, [])

                        df = pd.read_excel(file_path, sheet_name=sheet_name, na_values=['NA'])
                        # print(f'================== sheet_name {sheet_name} =================')
                        max_jod, max_res = [], [] # max_jod in all refresh rates
                        # type1(df, bitrate_dict[bitrate], len(refresh_rate), refresh_rate, bitrate, SAVE)
                        type2(df, bitrate_dict[bitrate], bitrate, len(refresh_rate), refresh_rate, SAVE)
                        max_idx = np.argmax(max_jod) # only availble if type2 is run
                        max_jod_val = max_jod[max_idx]
                        # print(f'\nmax_jod {max_jod} max_res {max_res}')
                        # print(f'bitrate {bitrate}, max JOD is {max_jod[max_idx]} with resolution {max_res[max_idx]} fps {refresh_rate[max_idx]}')
                        # max_comb_per_bitrate[sequence_name].append([refresh_rate[max_idx], max_res[max_idx]])
                        
                        # output is like: max_comb_per_sequence {'path1_seg2_3': [[80, 480, 7.1158], [120, 720, 7.5596], [120, 720, 7.7879], [120, 720, 7.9228]]}
                        max_comb_per_sequence[sheet_name].append([refresh_rate[max_idx], max_res[max_idx], max_jod[max_idx]])

                        comb_per_sheet = find_comb_within_range(df, bitrate_dict[bitrate], bitrate, max_comb_per_sequence[sheet_name])
                        comb_within_range_per_sequence[sheet_name].append(comb_per_sheet)
                        


                        # print(f'max_comb_per_bitrate {max_comb_per_bitrate}')
            # print(f'{bitrate}kbps {max_comb_per_bitrate}')
        # print(f'max_comb_per_sequence {max_comb_per_sequence}')
        # print(f'comb_within_range_per_sequence \n{comb_within_range_per_sequence}')

        if WRITE_DICT:
            with open(f"fps_res_drop_jod_THRESOLD{int(THRESHOLD*100)}-{time_path}.py", "a") as file:
                file.write("\n") 
                file.write(f"{scene_name}_within_JOD_range = {comb_within_range_per_sequence}")