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

class_table = {0: 'face' , 1:'person' , 2:'upperbody'}

color_init()

titleBox('IVIEW+ (HDS-K01/K02) BBOX 조건 추출')

parser = argparse.ArgumentParser(description='IVIEW+ (HDS-K01/K02) BBOX 조건 추출')

parser.add_argument('-i', '--input', type = str, help='Input Directory', required = True)
parser.add_argument('-o', '--output', type = str, help='Output Directory', required = True)

parser.add_argument('-c', '--objectclass', choices=['face', 'person', 'upperbody'], help='Class', required = True)
parser.add_argument('-s', '--size', type = float, help='Reference Size')
parser.add_argument('-r', '--ratio', type = float, help='Reference Ratio')

parser.add_argument('-g', '--greater', action = 'store_true', help='Greater thsan Reference Size')
parser.add_argument('-l', '--less', action = 'store_true', help='Less thsan Reference Size')

args = parser.parse_args()

input_dir = args.input
output_dir = args.output

if input_dir[-1] != '/':
    input_dir += '/'
if output_dir[-1] != '/':
    output_dir += '/'

target_class = args.objectclass
target_size = args.size
target_ratio = args.ratio
target_condition = None

if target_size and not target_ratio:
    target_condition = 'size'
    target_reference = target_size
elif not target_size and target_ratio:
    target_condition = 'ratio'
    target_reference = target_ratio

if args.greater and not args.less:
    target_direction = 'Greater'
elif not args.greater and args.less:
    target_direction = 'Less'
else:
    print('Greater and Less condition cannot co-exist')
    exit()

messageBox(' Class={0}, Condition={1}, Reference={2}, Direction={3}'.format(target_class, target_condition, target_reference, target_direction))

all_input_files = glob.glob(input_dir + '*.txt')

matched_file = 0

Path(output_dir).mkdir(parents=True, exist_ok=True)


for filename in all_input_files:

    with open(filename,'r') as file:

        bboxes = []

        new_lines = []
        new_file = False

        condition_match = False

        for line in file:

            fields = line.split(' ')
            
            #x_center y_center width height

            bbox_info = {'class' : int(fields[0]), 'x_center' : float(fields[1]), 'y_center' : float(fields[2]), 'width' : float(fields[3]), 'height' : float(fields[4])}       
            #bbox_info = {'class' : int(fields[0]), 'xs' : float(fields[1]), 'xe' : float(fields[2]), 'ys' : float(fields[3]), 'ye' : float(fields[4]), 'cs' : float(fields[5])}
            
            
            try:
                size = bbox_info['width'] * bbox_info['height']
                ratio = bbox_info['width'] / bbox_info['height']

                if class_table[bbox_info['class']] == target_class:

                    if target_condition == 'size':
                        compare_value = size
                    else:
                        compare_value = ratio

                    #messageBox('Compare value = {0}'.format(compare_value))
                    if target_direction == 'Greater' and compare_value > target_reference:
                            condition_match = True

                    if target_direction == 'Less' and compare_value <= target_reference:
                            condition_match = True

            except:
                messageBox('Filename {0} has wrong information'.format(filename))
                messageJSON(bbox_info)
                #exit()
            


        if condition_match:
            messageBox ('Filename {0} has matched the condition'.format(filename))
            
            base_filename = os.path.basename(filename)[:-4]
            #copyfile(self.file)        
           
            try:
                copyfile(input_dir+'\\'+base_filename+'.jpg', output_dir+'\\'+base_filename+'.jpg')
                copyfile(input_dir+'\\'+base_filename+'.txt', output_dir+'\\'+base_filename+'.txt')
            except:
                pass
            matched_file+=1

messageBox ('Total matched file {0} out of {1}'.format(matched_file, len(all_input_files)))

"""
# absolute path to search all text files inside a specific folder
all_group_files = glob.glob(group_dir + '*.*')
all_subgroup_files = glob.glob(subgroup_dir + '*.*')

all_group_base_files = []
all_subgroup_base_files = []

for file in all_group_files:
    all_group_base_files.append(os.path.basename(file))

for file in all_subgroup_files:
    all_subgroup_base_files.append(os.path.basename(file))

exclusive_files = list(set(all_group_base_files)-set(all_subgroup_base_files))

#self.files = glob.glob(r'./data/*.jpg')
file_idx = 0
file_max = len(exclusive_files)

Path(output_dir).mkdir(parents=True, exist_ok=True)

for filename in exclusive_files:

        #copyfile(self.file)        
    print('Copy file : {0}'.format(filename))

    copyfile(group_dir+'\\'+filename, output_dir+'\\'+filename)
    
"""