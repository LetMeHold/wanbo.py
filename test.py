from gl import *
from wrap import *
from openpyxl import Workbook
from openpyxl import load_workbook
import pymysql.cursors

GL.LOG = getLogger('WanboLoger', 'logs', 'console.log')
db = DB(db='wanbo')

def TestDB():
    sql = 'select * from test'
    print(db.query(sql))

def InsertToBalance(mp):
    keys_sql = '('
    values_sql = '('
    for k,v in mp.items():
        keys_sql += '%s,' % k
        if v == None:
            values_sql += 'NULL,'
        elif isinstance(v, str):
            values_sql += '\'%s\',' % v
        else:
            values_sql += '%s,' % v
    keys_sql = keys_sql.rstrip(',')
    values_sql = values_sql.rstrip(',')
    keys_sql += ')'
    values_sql += ')'
    sql = 'insert into balance %s values%s' % (keys_sql,values_sql)
    db.exec(sql)
    
def InsertToAccount(mp):
    keys_sql = '('
    values_sql = '('
    for k,v in mp.items():
        keys_sql += '%s,' % k
        if v==None or v=='-' or v=='/':
            values_sql += 'NULL,'
        elif isinstance(v, str):
            values_sql += '\'%s\',' % v
        else:
            values_sql += '%s,' % v
    keys_sql = keys_sql.rstrip(',')
    values_sql = values_sql.rstrip(',')
    keys_sql += ')'
    values_sql += ')'
    sql = 'insert into account %s values%s' % (keys_sql,values_sql)
    #print(sql)
    db.exec(sql)

def ReadBalanceData(source):
    n = 0
    mp = {}
    for row in ws.rows:
        n = n + 1
        if n <= 3:
            continue
        if n == 10:
            break
        if len(row) < 12:
            return
        mp['class1'] = row[0].value
        if mp['class1']==None or mp['class1'].strip()=='':
            return
        mp['class2'] = row[1].value
        year = row[2].value
        month = row[3].value
        day = row[4].value
        mp['date'] = '%d-%d-%d' % (year,month,day)
        mp['abstract'] = row[5].value
        mp['income'] = row[6].value
        mp['pay'] = row[7].value
        mp['balance'] = row[8].value
        mp['type'] = row[9].value
        mp['credence'] = row[10].value
        mp['remark'] = row[11].value
        mp['source'] = source
        InsertToBalance(mp)

def ReadAccountData():
    n = 0
    mp = {}
    for row in ws.rows:
        n = n + 1
        if n <= 3:
            continue
        if n == 20:
            break
        if len(row) < 18:
            return
        mp['no'] = row[0].value
        year = row[1].value
        if isinstance(mp['no'],int)==False or isinstance(year,int)==False:
            continue
        del mp['no']
        month = row[2].value
        day = row[3].value
        mp['date'] = '%d-%d-%d' % (year,month,day)
        mp['seller'] = row[4].value
        mp['contract'] = row[5].value
        mp['client'] = row[6].value
        mp['amount'] = row[7].value
        mp['paid'] = row[8].value
        mp['unpaid'] = row[9].value
        mp['debt'] = row[10].value
        mp['percent'] = row[11].value
        mp['invoice_commission'] = row[12].value
        mp['invoice_type'] = row[13].value
        mp['invoice_paid'] = row[14].value
        mp['invoice_unpaid'] = row[15].value
        mp['status'] = row[16].value
        mp['unpaid_reason'] = row[17].value
        mp['commission'] = row[18].value
        mp['commission_date'] = row[19].value
        mp['remark'] = row[20].value
        InsertToAccount(mp)

fn = '../../db/wanbo/2018财务汇总表（46周）.xlsx'
wb = load_workbook(fn, read_only=True, data_only=True)
for ws in wb:
    if ws.title == '应收账款汇总表':
        ReadAccountData()
    elif ws.title == '银行明细账':
        source = '建设银行（基本户）'
        ReadBalanceData(source)
    elif ws.title == '现金账户1明细账':
        source = '平安银行（姚洋）'
        ReadBalanceData(source)
    elif ws.title == '现金账户2明细账':
        source = '平安银行（李昱平）'
        ReadBalanceData(source)
    else:
        pass
del db
#time.sleep(3)
#db.close()
