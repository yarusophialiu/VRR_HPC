import os




BASE_DIR = "bistro"
SCENE = "bistro"
CLEANED_DIR = "cleaned"

DELETE = True # False True

if DELETE:
    # for bitrate in bitrates:
        input_scene_path = f"{SCENE}"
        cleaned_scene_path = f'{CLEANED_DIR}/{SCENE}'
        os.makedirs(cleaned_scene_path, exist_ok=True)
        jobid_list = [i for i in range(1, 24)]

        for jobid in jobid_list:
            print(f'===== jobid {jobid} =====')
            input_file_path = f'{input_scene_path}/{SCENE}_{jobid}.txt'
            output_file_path = f'{cleaned_scene_path}/{SCENE}_{jobid}.txt'

            if not os.path.exists(input_file_path):
                print(f"jobid {jobid}, input file {input_file_path} NOT exists, skip.")
                continue

            if os.path.exists(output_file_path):
                print(f"jobid {jobid}, output file {output_file_path} exists, skip.")
                continue

            with open(input_file_path, "r") as file:
                lines = file.readlines()

            filtered_lines = [line for line in lines if not line.strip().lower().startswith(('current', 'dec_file', '/home/yl962/rds'))]
            # filtered_lines = [line for line in lines if line.strip()]

            with open(output_file_path, "w") as file:
                for line in filtered_lines:
                    if ("Command executed successfully." not in line) and line.strip():
                        file.write(line)


