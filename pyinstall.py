import PyInstaller.__main__
#from PIL import Image
import os
#import sys

icon_path_abs = os.path.abspath('zicon.png')
PyInstaller.__main__.run([
    'main.py',
    '--windowed',
    '--noconsole',
    f'--icon={icon_path_abs}',
])
