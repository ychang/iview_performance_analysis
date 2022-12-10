#!/usr/local/bin/python3.6

"""
Docstring Usage

Use these keyboard shortcuts, or the commands below from the Command Pallete.

<cmd + alt + '> will update a docstring for the first module/class/function preceding the cursor.
<cmd + alt + shift + '> will update docstrings for every class/method/function in the current file
"""

import os
import argparse
import glob
import numpy
import time
from datetime import datetime

from pathlib import Path

from iview_utils import *

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

from shutil import copyfile

color_init()

titleBox('IVIEW+ (HDS-K01/K02) 비중복 파일 추출')

parser = argparse.ArgumentParser(description='IVIEW+ (HDS-K01/K02)  비소속 데이터 추출')

parser.add_argument('-g', '--group', type = str, help='Source Group Directory', required = True)
parser.add_argument('-s', '--subgroup', type = str, help='Sub-Group Directory', required = True)
parser.add_argument('-o', '--output', type = str, help='Output Directory', required = True)

args = parser.parse_args()

group_dir = args.group
subgroup_dir = args.subgroup
output_dir = args.output

if group_dir[-1] != '/':
    group_dir += '/'
if subgroup_dir[-1] != '/':
    subgroup_dir += '/'
if output_dir[-1] != '/':
    output_dir += '/'

# absolute path to search all text files inside a specific folder
all_group_files = glob.glob(group_dir + '*.*')
all_subgroup_files = glob.glob(subgroup_dir + '*.*')

all_group_base_files = []
all_subgroup_base_files = []

for file in all_group_files:
    all_group_base_files.append(os.path.basename(file))

for file in all_subgroup_files:
    all_subgroup_base_files.append(os.path.basename(file)[4:])

exclusive_files = list(set(all_group_base_files)-set(all_subgroup_base_files))

#self.files = glob.glob(r'./data/*.jpg')
file_idx = 0
file_max = len(exclusive_files)

Path(output_dir).mkdir(parents=True, exist_ok=True)

for filename in exclusive_files:

        #copyfile(self.file)        
    print('Copy file : {0}'.format(filename))

    copyfile(group_dir+'\\'+filename, output_dir+'\\'+filename)
    
