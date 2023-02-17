'''Task_2'''
def report_2(curs, DT):
    '''Building a report on task_2'''
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