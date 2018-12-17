from gl import *
from wrap import *
import pymysql.cursors
from openpyxl import Workbook
from openpyxl import load_workbook

GL.LOG = getLogger('WanboLoger', 'logs', 'console.log')
GL.LOG.info('测试')

wb = Workbook()
ws = wb.active
row = 0
col = 0
ws.cell(row=1,column=1).value = 42
ws.cell(row=2,column=2).value = 42

wb.save('x.xlsx')

