import os

def count_files_in_subfolders(root_directory):
    # Traverse the directory tree starting from the root directory
    for root, dirs, files in os.walk(root_directory):
        print(f'dirs {dirs}')
        for dir_name in dirs:
            # Get the full path of the subfolder
            subfolder_path = os.path.join(root, dir_name)
            # Count the number of files in the subfolder
            file_count = sum([len(files) for _, _, files in os.walk(subfolder_path)])
            print(f"Subfolder: {subfolder_path}, File count: {file_count}")
            os.chdir(f'/home/yl962/rds/hpc-work/VRR/VRRMP4_CVVDP/crytek_sponza/{dirs}')
            current_directory = os.getcwd()
            print(f"Current working directory: {current_directory}")

if __name__ == "__main__":
    # Define the root directory (update this to your actual path)
    root_directory = r'C:\path\to\source\directory'
    # Run the count operation
    count_files_in_subfolders(root_directory)
