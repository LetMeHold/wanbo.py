# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit',
        'include_files': 'res'
    }
}

executables = [
    Executable(base=base, script='main.py', targetName='wanbo.exe', icon='res/logo.ico')
]

setup(name='wanbo',
      version='0.9.0',
      description='wanbo system',
      options=options,
      executables=executables
)

