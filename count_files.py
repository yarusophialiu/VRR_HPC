import os
import subprocess

def count_files_in_subfolders(root_directory):
    # Traverse the directory tree starting from the root directory
    print(f'root directory {root_directory}')
    count = 0

    for root, dirs, files in os.walk(root_directory):
        dirs.sort()
        print(f'Sorted dirs: {dirs}')
        for dir_name in dirs:
            # Get the full path of the subfolder
            subfolder_path = os.path.join(root, dir_name)
            # Change the current working directory to the subfolder
            os.chdir(subfolder_path)
            # Run the 'find . -type f | wc -l' command
            result = subprocess.run(['find', '.', '-type', 'f'], capture_output=True, text=True)
            file_count = len(result.stdout.splitlines())
            count += file_count
            print(f"Subfolder: {subfolder_path}, File count: {file_count}, count: {count}")
            # file_count = sum([len(files) for _, _, files in os.walk(subfolder_path)])
            # print(f"Subfolder: {subfolder_path}, File count: {file_count}")
            # os.chdir(f'/home/yl962/rds/hpc-work/VRR/VRRMP4_CVVDP/crytek_sponza/{dirs}')
            # current_directory = os.getcwd()
            # print(f"Current working directory: {current_directory}")

if __name__ == '__main__':
    # Define the root directory
    root_directory = r'suntemple'
    print(f'root dir {root_directory}')
    # Run the count operation
    count_files_in_subfolders(root_directory)