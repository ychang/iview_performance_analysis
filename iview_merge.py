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

from colorama import init as colorama_init
from colorama import Fore, Back, Style

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

# Definitions
INTERACTIVE = 0
BATCH       = 1
output_dir_check = False
cnt=[]
List=[]


color_code = {0: 'darkred', 1 : 'orange', 2: 'green'}
text_color_code = {0: 'red', 1 : 'yellow', 2: 'lime'}
class_code = {'face' : 0, 'person' : 1, 'upperbody' : 2}



class ImageProcess:
    """A simple example class
    
    Attributes:
        file (TYPE): Description
        file_idx (int): Description
        file_max (TYPE): Description
        files (TYPE): Description
    """

    def __init__(self, input_dir, output_dir):
        
        all_jpgs = input_dir + '*.jpg'
        
        # absolute path to search all text files inside a specific folder
        self.files = glob.glob(all_jpgs)
        #self.files = glob.glob(r'./data/*.jpg')
        self.file_idx = 0
        self.file_max = len(self.files)

        self.file = self.files[self.file_idx][:-4]
        
        self.output_dir = output_dir
        self.output_dir_check = False

        print('{0} files found.'.format(self.file_max))

    def print_files(self):
        print('Files : ', self.files)


    def next(self):

        if self.file_idx < self.file_max-1:
            self.file_idx += 1
            self.file = self.files[self.file_idx][:-4]
            return self.file
        else:
            return None

    def prev(self):

        if self.file_idx > 0:
            self.file_idx -= 1
            self.file = self.files[self.file_idx][:-4]

        return self.file

    def save_current_figure(self):

        if not self.output_dir_check:
            Path(self.output_dir).mkdir(parents=True, exist_ok=True)
            self.output_dir_check = True

            with open(self.output_dir+'_parameters.txt', 'w') as f:
                now = datetime.now()
                f.write('DateTime   : '+now.strftime("%Y/%m/%d %H:%M:%S")+'\r\n')
                f.write('Input Dir  : '+input_dir+'\r\n')
                f.write('Output Dir : '+output_dir+'\r\n')
                f.write('CS File    : '+cs_file+'\r\n')

        print('Save file '+os.path.basename(self.file))
        plt.savefig(self.output_dir+os.path.basename(self.file))


def messageBox(note, color=Fore.WHITE):

    print('{0}{1}{2}'.format(color, note, Style.RESET_ALL))

def messageDebug(note, color=Fore.WHITE):

    if closing_configuration.DEBUG:
        print('{0}{1}{2}'.format(color, note, Style.RESET_ALL))

def titleBox(note, color=Fore.WHITE):

    messageBox('')
    messageBox('===========================================================================================', Fore.GREEN)
    messageBox(' '+note, color)
    messageBox('===========================================================================================', Fore.GREEN)

def messageJSON(dict_to_show):
    print( json.dumps(dict_to_show, indent=4, ensure_ascii=False) )

def draw_image(filename):
    """Summary
    
    Args:
        filename (TYPE): Description
    
    Returns:
        TYPE: Description
    """
    if filename[21:] not in cs_data:
        
        print ('File {0} doest not have a confidence score data'.format(filename))
        return

    try:
        with open(filename+'.txt','r') as file:

            bboxes = []

            for line, cs_info in zip(file, cs_data[filename[21:]]):

                fields = line.split(' ')
                
                #x_center y_center width height

                bbox_info = {'class' : int(fields[0]), 'x_center' : float(fields[1]), 'y_center' : float(fields[2]), 'width' : float(fields[3]), 'height' : float(fields[4]), 'cs' : cs_info['cs']}       
                #bbox_info = {'class' : int(fields[0]), 'xs' : float(fields[1]), 'xe' : float(fields[2]), 'ys' : float(fields[3]), 'ye' : float(fields[4]), 'cs' : float(fields[5])}
                bboxes.append(bbox_info)

    except Exception as error: 
        return


    img = mpimg.imread(filename+'.jpg')
    size_y = img.shape[0]
    size_x = img.shape[1]

    #plt.subplot(2, 2, 1)                # nrows=2, ncols=1, index=1

    ax1.set_title(os.path.basename(filename), fontsize=10)    
    img1.set_data(img)

    ax2.set_title('All confidence scores', fontsize=10)
    [p.remove() for p in reversed(ax2.patches)]
    [p.remove() for p in reversed(ax2.texts)]

    ax3.set_title('Confidence scores threshold = 0.6', fontsize=10)
    [p.remove() for p in reversed(ax3.patches)]
    [p.remove() for p in reversed(ax3.texts)]

    ax4.set_title('Confidence scores threshold = 0.7', fontsize=10)
    [p.remove() for p in reversed(ax4.patches)]
    [p.remove() for p in reversed(ax4.texts)]

    for bbox in bboxes:

        if bbox['cs'] >= 0.0:

            x_center = int(size_x*bbox['x_center'])
            y_center = int(size_y*bbox['y_center'])
            
            width = int(size_x*bbox['width'])
            height = int(size_y*bbox['height'])

            x_start = x_center - width/2
            y_start = y_center - height/2

            color = color_code[bbox['class']]
            text_color = text_color_code[bbox['class']]

            if bbox['cs'] >= 0.7:
                ax4.add_patch(Rectangle((x_start, y_start), width, height,  linewidth=2, edgecolor=color, fill = False))
                ax4.text(x_center, y_center, '{0}'.format(bbox['cs']), color = text_color)


            if bbox['cs'] >= 0.6:
                ax3.add_patch(Rectangle((x_start, y_start), width, height,  linewidth=2, edgecolor=color, fill = False))
                ax3.text(x_center, y_center, '{0}'.format(bbox['cs']), color = text_color)

            ax2.add_patch(Rectangle((x_start, y_start), width, height,  linewidth=2, edgecolor=color, fill = False))
            ax2.text(x_center, y_center, '{0}'.format(bbox['cs']), color = text_color)


def close_figure(event):
    if event.key == 'right':
        done = imgprc.next()

        if done == None:
            plt.close(event.canvas.figure)
        else:
            draw_image(done)

            # drawing updated values
            figure.canvas.draw()
            figure.canvas.flush_events()

    if event.key == 'left':
        done = imgprc.prev()

        if done == None:
            plt.close(event.canvas.figure)
        else:
            draw_image(done)

            # drawing updated values
            figure.canvas.draw()
            figure.canvas.flush_events()

    if event.key == 'w':

        imgprc.save_current_figure()


def read_confidence_score(filename):

    try:
        with open(filename,'r') as file:

            cs_data = {}
            for line in file:
                fields = line.split(' ')

                file_f = fields[2][24:-5]

                class_f = class_code[fields[0]]

                cs_f = float (fields[1])

                if file_f not in cs_data:
                    cs_data[file_f] = []

                cs_data[file_f].append ( {'class' : class_f, 'cs' : cs_f})

                #cs_info = {'class' : int(fields[0]), 'x_center' : float(fields[1]), 'y_center' : float(fields[2]), 'width' : float(fields[3]), 'height' : float(fields[4]), 'cs' : 0}       
                #bbox_info = {'class' : int(fields[0]), 'xs' : float(fields[1]), 'xe' : float(fields[2]), 'ys' : float(fields[3]), 'ye' : float(fields[4]), 'cs' : float(fields[5])}

            return cs_data

    except:
        return None

"""
def save_current_figure(filename):

    if not output_dir_check:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        output_dir_check = True

        with open(output_dir+'_parameters.txt', 'w') as f:
            now = datetime.now()
            f.write('DateTime   : '+now.strftime("%Y/%m/%d %H:%M:%S"))
            f.write('Input Dir  : '+input_dir)
            f.write('Output Dir : '+output_dir)
            f.write('CS File    : '+cs_file)

    print('Save file '+os.path.basename(filename))
    plt.savefig(output_dir+os.path.basename(ifilename))
"""

colorama_init()

titleBox('IVIEW+ (HDS-K01/K02) 학습데이터 CLASS MERGE (PERSON, UPPERBODY)')

parser = argparse.ArgumentParser(description='IVIEW+ (HDS-K01/K02) 학습데이터 CLASS MERGE (PERSON, UPPERBODY)')

parser.add_argument('-i', '--input', type = str, help='Inference Data Directory', required = True)
parser.add_argument('-o', '--output', type = str, help='Output Directory', required = True)

args = parser.parse_args()

input_dir = args.input
output_dir = args.output

if input_dir[-1] != '/':
    input_dir += '/'
if output_dir[-1] != '/':
    output_dir += '/'

print ('Input Dir = {0}'.format(input_dir))
print ('Output Dir = {0}'.format(output_dir))

all_texts = input_dir + '*.txt'

# absolute path to search all text files inside a specific folder
files = glob.glob(all_texts)
#self.files = glob.glob(r'./data/*.jpg')
file_idx = 0
file_max = len(files)

Path(output_dir).mkdir(parents=True, exist_ok=True)


for filename in files:

    with open(filename,'r') as file:

        output_filename = output_dir+os.path.basename(filename)

        if os.path.exists(output_filename):
            append_write = 'a' # append if already exists
        else:
            append_write = 'w' # make a new file if not

        with open(output_filename, append_write) as f:
            #for line in new_lines:
            #    f.write(line)

            bboxes = []

            new_lines = []
            new_file = False

            for line in file:

                fields = line.split(' ')
                
                #x_center y_center width height

                bbox_info = {'class' : int(fields[0]), 'x_center' : float(fields[1]), 'y_center' : float(fields[2]), 'width' : float(fields[3]), 'height' : float(fields[4])}       
                #bbox_info = {'class' : int(fields[0]), 'xs' : float(fields[1]), 'xe' : float(fields[2]), 'ys' : float(fields[3]), 'ye' : float(fields[4]), 'cs' : float(fields[5])}
                
                new_class = bbox_info['class']
                if new_class == 2:
                    new_class = 1

                new_line = "{0} {1} {2} {3} {4}\n".format(new_class, bbox_info['x_center'], bbox_info['y_center'], bbox_info['width'], bbox_info['height'])

                f.write(new_line)


