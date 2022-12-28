import pandas
import os
import glob
import re
import jaydebeapi as jdba

# Установка соединения с сервером
conn = jdba.connect(
'oracle.jdbc.driver.OracleDriver',
'jdbc:oracle:thin:demipt/gandalfthegrey@de-oracle.chronosavant.ru:1521/deoracle',
['user','password'],
'/home/demipt/ojdbc8.jar'
)

curs = conn.cursor()


os.chdir('/home/demipt/yupi')

#Поиск минимальной даты файлов-источников 
X = glob.glob('*.txt')
if len(X) > 1:
    X = min(re.findall("\d+", '{}'.format(X)))
else:
    X = ''.join(re.findall("\d+", '{}'.format(X)))
DT = X[4:8] + '-' + X[2:4] + '-' + X[0:2]

#Загрузка данных с терминалов
df = pandas.read_excel( 'terminals_' + X + '.xlsx', sheet_name='terminals', header=0, index_col=None )
df['create_dt'] = pandas.Series(DT, index=df.index)
curs.executemany( """insert into DEMIPT.YUPI_STG_TERMINALS ( TERMINAL_ID, TERMINAL_TYPE, TERMINAL_CITY, TERMINAL_ADDRESS, CREATE_DT ) values ( ?, ?, ?, ?, to_date(?,'YYYY-MM-DD')) """, df.values.tolist() )

#Загрузка данных транзакций
df = pandas.read_csv( 'transactions_' + X + '.txt', sep = ";", header=0, index_col=None )
df=df.reindex(columns=['transaction_id', 'transaction_date', 'card_num', 'oper_type', 'amount', 'oper_result', 'terminal'])
df['transaction_date'] = df['transaction_date'].astype(str)
curs.executemany( """insert into DEMIPT.YUPI_STG_TRANSACTIONS ( TRANS_ID, TRANS_DATE, CARD_NUM, OPER_TYPE, AMT, OPER_RESULT, TERMINAL ) values ( ?, to_date(?,'YYYY-MM-DD HH24:MI:SS'), ?, ?, ?, ?, ?) """, df.values.tolist() )

#Загрузка данных "Чёрного списка" паспортов
df = pandas.read_excel( 'passport_blacklist_' + X + '.xlsx', sheet_name='blacklist', header=0, index_col=None )
df = df.dropna(how='any',axis=0)
df = df.loc[df['date'] == DT]
df['date'] = df['date'].astype(str)
df=df.reindex(columns=['passport', 'date'])
curs.executemany( """insert into DEMIPT.YUPI_STG_PASSPORT_BLACKLIST ( PASSPORT_NUM, ENTRY_DT ) values ( ?, to_date(?,'YYYY-MM-DD')) """, df.values.tolist() )

# ETL
inc = open('sql_scripts\INCREMENTAL.sql').read().split(";")
for i in inc:
	curs.execute( i )

# Построение отчёта
curs.execute(('''insert into DEMIPT.YUPI_REP_FRAUD( EVENT_DT, PASSPORT, FIO, PHONE,EVENT_TYPE, REPORT_DT )
select
	min(t4.TRANS_DATE),
	t1.PASSPORT_NUM,
    max (t1.LAST_NAME ||' '|| t1.FIRST_NAME ||' '|| t1.PATRONYMIC),
	max(t1.PHONE),
	1,
	max(to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day)
from DEMIPT.YUPI_DWH_DIM_CLIENTS_HIST t1
left join DEMIPT.YUPI_DWH_DIM_ACCOUNTS_HIST t2 on t1.client_id = t2.client
left join DEMIPT.YUPI_DWH_DIM_CARDS_HIST t3 on t2.ACCOUNT = t3.ACCOUNT_NUM
left join DEMIPT.YUPI_DWH_FACT_TRANSACTIONS t4 on t3.CARD_NUM = t4.CARD_NUM and TRANS_DATE BETWEEN to_date( '{}', 'YYYY-MM-DD' ) and to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day
left join DEMIPT.YUPI_DWH_FACT_PSSPRT_BLCKLST t5 on t1.PASSPORT_NUM = t5.PASSPORT_NUM
where t1.PASSPORT_VALID_TO < to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day or t1.PASSPORT_NUM = t5.PASSPORT_NUM
group by t1.PASSPORT_NUM''').format(DT,DT,DT,DT))

curs.execute(('''insert into DEMIPT.YUPI_REP_FRAUD( EVENT_DT, PASSPORT, FIO, PHONE,EVENT_TYPE, REPORT_DT )
select
	min(t4.TRANS_DATE),
	t1.PASSPORT_NUM,
    max(t1.LAST_NAME ||' '|| t1.FIRST_NAME ||' '|| t1.PATRONYMIC),
	max(t1.PHONE),
	2,
	max(to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day)
from DEMIPT.YUPI_DWH_DIM_CLIENTS_HIST t1
left join DEMIPT.YUPI_DWH_DIM_ACCOUNTS_HIST t2 on t1.client_id = t2.client
left join DEMIPT.YUPI_DWH_DIM_CARDS_HIST t3 on t2.ACCOUNT = t3.ACCOUNT_NUM
left join DEMIPT.YUPI_DWH_FACT_TRANSACTIONS t4 on t3.CARD_NUM = t4.CARD_NUM and TRANS_DATE BETWEEN to_date( '{}', 'YYYY-MM-DD' ) and to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day
where t2.VALID_TO < to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day
group by t1.PASSPORT_NUM''').format(DT,DT,DT,DT))

curs.execute(('''insert into DEMIPT.YUPI_REP_FRAUD( EVENT_DT, PASSPORT, FIO, PHONE,EVENT_TYPE, REPORT_DT )
select
	max(TD),
	t1.PASSPORT_NUM,
    max(t1.LAST_NAME ||' '|| t1.FIRST_NAME ||' '|| t1.PATRONYMIC),
	max(t1.PHONE),
	3,
	max(to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day)
from DEMIPT.YUPI_DWH_DIM_CLIENTS_HIST t1
left join DEMIPT.YUPI_DWH_DIM_ACCOUNTS_HIST t2 on t1.client_id = t2.client
left join DEMIPT.YUPI_DWH_DIM_CARDS_HIST t3 on t2.ACCOUNT = t3.ACCOUNT_NUM
left join 
(select
    t.*,
    max(TD) over (PARTITION BY CARD_NUM) - min(TD) over (PARTITION BY CARD_NUM) as MN
from (
select distinct
    t1.CARD_NUM,
    count(DISTINCT TERMINAL_CITY) over (PARTITION BY CARD_NUM) as CN,
    FIRST_VALUE(TRANS_DATE) over (PARTITION BY TERMINAL_CITY) as TD,
    t2.terminal_city 
from YUPI_DWH_FACT_TRANSACTIONS t1
left join YUPI_DWH_DIM_TERMINALS_HIST t2
on t1.terminal = t2.terminal_id
where TRANS_DATE BETWEEN to_date( '{}', 'YYYY-MM-DD' ) and to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day) t
where CN > 1) t4 on t3.CARD_NUM = t4.CARD_NUM
where MN < 1/24
group by t1.PASSPORT_NUM''').format(DT,DT,DT))

curs.execute(('''insert into DEMIPT.YUPI_REP_FRAUD( EVENT_DT, PASSPORT, FIO, PHONE,EVENT_TYPE, REPORT_DT )
select
	TD,
	t1.PASSPORT_NUM,
    max(t1.LAST_NAME ||' '|| t1.FIRST_NAME ||' '|| t1.PATRONYMIC),
	max(t1.PHONE),
	4,
	max(to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day)
from DEMIPT.YUPI_DWH_DIM_CLIENTS_HIST t1
left join DEMIPT.YUPI_DWH_DIM_ACCOUNTS_HIST t2 on t1.client_id = t2.client
left join DEMIPT.YUPI_DWH_DIM_CARDS_HIST t3 on t2.ACCOUNT = t3.ACCOUNT_NUM
inner join 
(select t2.* from (
select 
    t1.*,
    TRANS_DATE - lag(TRANS_DATE) over (PARTITION BY CARD_NUM ORDER BY CARD_NUM,TRANS_DATE) as DiffDT,
    count(M) over (PARTITION BY CARD_NUM) as NUM,
    MAX(TRANS_DATE) over (PARTITION BY CARD_NUM) as TD
from ( 
select
    TRANS_ID,
    TRANS_DATE,
    CARD_NUM,
    AMT,
    AMT - lag(AMT,1,0) over (PARTITION BY CARD_NUM ORDER BY CARD_NUM,TRANS_DATE) as M,
    OPER_RESULT
from YUPI_DWH_FACT_TRANSACTIONS
where TRANS_DATE BETWEEN to_date( '{}', 'YYYY-MM-DD' ) and to_date( '{}', 'YYYY-MM-DD' ) + interval '1' day and OPER_TYPE = 'WITHDRAW' and OPER_RESULT = 'REJECT'
) t1
where M < 0
) t2
where NUM > 2 and DiffDT < 1/288 ) t4 on t3.CARD_NUM = t4.CARD_NUM
group by t1.PASSPORT_NUM,TD''').format(DT,DT,DT))

# Перемещение отработанных файлов
os.rename('terminals_' + X + '.xlsx', 'archive/terminals_' + X + '.xlsx.backup')
os.rename('transactions_' + X + '.txt', 'archive/transactions_' + X + '.txt.backup')
os.rename('passport_blacklist_' + X + '.xlsx', 'archive/passport_blacklist_' + X + '.xlsx.backup')

# Закрытие соединения
curs.close()
conn.close()

