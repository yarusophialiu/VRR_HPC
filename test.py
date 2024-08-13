import os
import re
from utils import *
from datetime import date





if __name__ == "__main__":
    # Define the root directory (update this to your actual path)
    # root_directory = r'C:\path\to\source\directory'
    # # Run the count operation
    # count_files_in_subfolders(root_directory)
    s1 = '========================='
    s2 = '========================='
    # print(mapIdToPath(0))
    # print(mapIdToPath(16))
    # sheet_name = 'path1_seg1_1'
    # print(sheet_name.split('_'))
    # print(os.listdir("cvvdp_results"))

    now = date.today()
    print(now)
    fps_sections = ['', '100', '\ncvvdp=3.1223 [JOD]\ncvvdp=5.5644 [JOD]\ncvvdp=5.6804 [JOD]\ncvvdp=5.5563 [JOD]\ncvvdp=5.3198 [JOD]\n', 
                    '110', '\ncvvdp=3.1503 [JOD]\ncvvdp=5.5934 [JOD]\ncvvdp=5.7020 [JOD]\ncvvdp=5.6055 [JOD]\ncvvdp=5.2011 [JOD]\n', 
                    '120', '\ncvvdp=3.0732 [JOD]\ncvvdp=-0.6765 [JOD]\ncvvdp=5.6939 [JOD]\ncvvdp=5.6077 [JOD]\ncvvdp=5.0213 [JOD]\n']
    cvvdp_values1 = re.findall(r'cvvdp=([-]?\d+\.\d+)', fps_sections[6])
    cvvdp_values2 = re.findall(r'cvvdp=([-]?\d+\.\d+)', fps_sections[2])
    cvvdp_values3 = re.findall(r'cvvdp=([-]?\d+\.\d+)', fps_sections[4]) # r'cvvdp=([-]?\d+\.\d+)'

    print(f'cvvdp_values1 \n {cvvdp_values1}')
    print(f'cvvdp_values2 \n {cvvdp_values2}')
    print(f'cvvdp_values3 \n {cvvdp_values3}')