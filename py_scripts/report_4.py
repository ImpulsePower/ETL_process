def report_4(curs, DT):
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