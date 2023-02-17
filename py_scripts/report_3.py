'''Task_3'''
def report_3(curs, DT):
    '''Building a report on task_3'''
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