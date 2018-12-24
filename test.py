# -*- coding: utf-8 -*-

from gl import *
from wrap import *
import pymysql.cursors
from openpyxl import Workbook
from openpyxl import load_workbook

GL.LOG = getLogger('WanboLoger', 'logs', 'console.log')
GL.LOG.info('测试')

mp = {'a':1,'b':2}
t = {'a':mp.copy(),'b':mp.copy()}

print(t['a']['a'])
print(t['b']['a'])
t['a']['a'] += 1
t['a']['a'] += 1
print(t['a']['a'])
print(t['b']['a'])

