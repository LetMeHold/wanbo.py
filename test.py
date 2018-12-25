# -*- coding: utf-8 -*-

from gl import *
from wrap import *
import pymysql.cursors
from openpyxl import Workbook
from openpyxl import load_workbook

GL.LOG = getLogger('WanboLoger', 'logs', 'console.log')
GL.LOG.info('测试')


