#!/usr/local/bin/python3.6

"""
Docstring Usage

Use these keyboard shortcuts, or the commands below from the Command Pallete.

<cmd + alt + '> will update a docstring for the first module/class/function preceding the cursor.
<cmd + alt + shift + '> will update docstrings for every class/method/function in the current file
"""
from colorama import init as colorama_init
from colorama import Fore, Back, Style

import json
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

def color_init():
    colorama_init()