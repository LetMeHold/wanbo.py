from gl import *
from wrap import *
from openpyxl import Workbook
from openpyxl import load_workbook
import pymysql.cursors
import datetime

GL.LOG = getLogger('WanboLoger', 'logs', 'console.log')
db = DB(db='wanbo')

def TestDB():
    sql = 'select * from test'
    print(db.query(sql))

def insertToTable(mp, table):
    keys_sql = '('
    values_sql = '('
    for k,v in mp.items():
        keys_sql += '%s,' % k
        if v==None or v=='-' or v=='/':
            values_sql += 'NULL,'
        elif isinstance(v, str):
            if v.strip() == '':
                values_sql += 'NULL,'
            else:
                values_sql += '"%s",' % v
        elif isinstance(v, datetime.datetime):
            values_sql += '"%s",' % v.strftime('%Y-%m-%d')
        else:
            values_sql += '%s,' % v
    keys_sql = keys_sql.rstrip(',')
    values_sql = values_sql.rstrip(',')
    keys_sql += ')'
    values_sql += ')'
    sql = 'insert into %s %s values%s' % (table,keys_sql,values_sql)
    #print(sql)
    db.exec(sql)

def ReadBalanceData(source):
    n = 0
    mp = {}
    for row in ws.rows:
        n = n + 1
        if n <= 3:
            continue
        if n == 500:
            break
        if len(row) < 18:
            continue
        mp['class1'] = row[0].value
        if mp['class1']==None or mp['class1'].strip()=='':
            continue
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
        insertToTable(mp, 'balance')

def ReadAccountData():
    n = 0
    mp = {}
    for row in ws.rows:
        n = n + 1
        if n <= 3:
            continue
        if n == 40:
            break
        if len(row) < 18:
            continue
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
        insertToTable(mp, 'account')

def ReadContractData():
    n = 0
    mp = {}
    for row in ws.rows:
        n = n + 1
        if n <= 4:
            continue
        if n == 10:
            break
        if len(row) < 18:
            continue
        mp['contract'] = row[1].value
        mp['date'] = row[2].value
        mp['seller'] = row[3].value
        mp['client'] = row[4].value
        mp['product'] = row[5].value
        mp['model'] = row[6].value
        mp['unit'] = row[7].value
        mp['quantity'] = row[8].value
        mp['price'] = row[9].value
        mp['count'] = row[10].value
        mp['amount'] = row[11].value
        mp['tax_rate'] = row[12].value
        mp['date_plan'] = row[13].value
        mp['date_actual'] = row[14].value
        mp['ontime'] = row[15].value
        mp['ontime_whynot'] = row[16].value
        mp['project'] = row[17].value
        mp['province'] = row[18].value
        mp['remark'] = row[19].value
        insertToTable(mp, 'contract')

def ReadInvoiceData():
    n = 0
    mp = {}
    for row in ws.rows:
        n = n + 1
        if n <= 2:
            continue
        if n == 100:
            break
        if len(row) < 16:
            continue
        mp['contract'] = row[0].value
        year = row[1].value
        month = row[2].value
        day = row[3].value
        mp['date'] = '%d-%d-%d' % (year,month,day)
        mp['invoice_no'] = row[4].value
        mp['invoice_client'] = row[5].value
        mp['invoice_content'] = row[6].value
        mp['model'] = row[7].value
        mp['quantity'] = row[8].value
        mp['price'] = row[9].value
        mp['price_notax'] = row[10].value
        mp['tax'] = row[11].value
        mp['amount'] = row[12].value
        mp['invoice_amount'] = row[13].value
        mp['invoice_type'] = row[14].value
        mp['status'] = row[15].value
        mp['refund'] = row[16].value
        mp['remark'] = row[17].value
        insertToTable(mp, 'invoice')

fn = '../../db/wanbo/2018财务汇总表（46周）.xlsx'
wb = load_workbook(fn, read_only=True, data_only=True)
for ws in wb:
    #if ws.title == '开票明细表':
        #ReadInvoiceData()
    #elif ws.title == '合同明细':
        #ReadContractData()
    #if ws.title == '应收账款汇总表':
        #ReadAccountData()
    if ws.title == '银行明细账':
        source = '建设银行（基本户）'
        ReadBalanceData(source)
    #elif ws.title == '现金账户1明细账':
        #source = '平安银行（姚洋）'
        #ReadBalanceData(source)
    #elif ws.title == '现金账户2明细账':
        #source = '平安银行（李昱平）'
        #ReadBalanceData(source)
    else:
        pass
del db
#time.sleep(3)
#db.close()
