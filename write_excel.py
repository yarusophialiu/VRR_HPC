import pandas as pd
import re
import os

def get_data(parts):
    fps_categories = []
    values_dict = {}
    current_fps = None
    for part in parts:
        if part.isdigit():
            current_fps = int(part)
            fps_categories.append(current_fps)
            values_dict[current_fps] = []
        else:
            # Extract values
            new_values = re.findall(r'cvvdp=([\d\.]+)', part)
            
        if current_fps and new_values:
            correct_order = new_values[1:] + new_values[:1]
            values_dict[current_fps].extend(correct_order)
            # print(f'new_values {new_values}')
            # print(f'correct_order {correct_order}\n')
            current_fps = None
    return fps_categories, values_dict

def create_df(fps_categories, values_dict):
    df = pd.DataFrame(columns=all_columns)
    df.loc[0] = [None] * len(all_columns)  # Initialize a new row with Nones

    # Insert the values into the DataFrame
    for fps in fps_categories:
        start_index = all_columns.index(360) + fps_categories.index(fps) * len(base_columns)
        end_index = start_index + len(base_columns)
        num_values = min(len(values_dict[fps]), len(base_columns))

        df.iloc[0, start_index:end_index] = values_dict[fps][:num_values] # row column  
    return df



def write_to_excel(df, excel_path):
    # if not os.path.exists(excel_path):
    mode = 'w'  if not os.path.exists(excel_path) else 'a'

    with pd.ExcelWriter(excel_path, engine='openpyxl', mode=mode, if_sheet_exists='overlay') as writer:

        if sheet_name in writer.book.sheetnames:
        # if mode == 'a' and sheet_name in writer.book.sheetnames:
            # Load existing Sheet X
            startrow = writer.book[sheet_name].max_row
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False, startrow=startrow)
        else:
            df.to_excel(writer, sheet_name=sheet_name, index=False)



# close excel file to write data to it
if __name__ == "__main__":
    # BASE_DIR = "bistro"
    SCENE = "bistro"
    CLEANED_DIR = "cleaned"

    cleaned_scene_path = f'{CLEANED_DIR}/{SCENE}'

    bitrates = [500,]
    speed = 1
    seg = 1
    # sheet_name = f'{scene}{speed}'
    # cvvdp_dir = f'06-14/{scene}{speed}'
    excel_dir = r'C:\Users\15142\Projects\VRR\VRR_Plot_HPC'
    # excel_path = f'{excel_dir}/{scene}-05-21.xlsx'
    excel_path = f'{excel_dir}/data-08-09/bistro.xlsx'
    sheet_name = f'path1_seg{seg}_{speed}'
    # cvvdp_dir = f'06-25/{SCENE}/{SCENE}_{sheet_name}'

    jobid_list = [i for i in range(1, 2)]
    for jobid in jobid_list:
        file_path = f'{cleaned_scene_path}/{SCENE}_{jobid}.txt'

        # Read the entire file into a string
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Use regular expressions to find sections by bitrate
        pattern = r"========================= bitrate (\d+) =========================(.*?)((?========================== bitrate)|$)"
        matches = re.findall(pattern, content, re.DOTALL)
        # print(f'matches \n{matches}')


        bitrate_data = {}
        for match in matches:
            bitrate = int(match[0])
            data = match[1].strip()

            # Split the data by fps
            fps_sections = re.split(r'========================= fps(\d+) =========================', data)
            fps_data = {}
            for i in range(1, len(fps_sections), 2):
                fps = int(fps_sections[i])
                cvvdp_values = re.findall(r'cvvdp=([\d\.]+)', fps_sections[i+1])
                fps_data[fps] = list(map(float, cvvdp_values))

            bitrate_data[bitrate] = fps_data # fps_data is like values_dict

            fps_categories = list(fps_data.keys())
            print(f'bitrate {bitrate}, fps data \n {fps_data}')
            print(f'fps_categories {list(fps_data.keys())}\n\n\n')

        
            # fps_categories, values_dict = get_data(parts)
            # # print(f'values_dict {values_dict}')
            fps_categories = sorted(fps_categories)
            print(f'fps_categories {fps_categories}')

            base_columns = [360, 480, 720, 864, 1080]
            all_columns = base_columns * 10
            df = create_df(fps_categories, fps_data)

            # TODO: create sheet if sheet not exist
            excel_df = pd.read_excel(excel_path, sheet_name=sheet_name)

            df.insert(0, 'bitrate', bitrate)

            write_to_excel(df, excel_path) # 360, 480, 720, 864, 1080

            # TODO: insert fps to line 18

