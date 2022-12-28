CREATE TABLE DEMIPT.YUPI_STG_TRANSACTIONS (   
    TRANS_ID VARCHAR2( 20 BYTE ), 
	TRANS_DATE DATE, 
	CARD_NUM CHAR( 20 BYTE ), 
	OPER_TYPE VARCHAR2 ( 20 BYTE ), 
	AMT NUMBER(32,2),
    OPER_RESULT VARCHAR2 ( 20 BYTE ),
    TERMINAL VARCHAR2 ( 20 BYTE )
);
CREATE TABLE DEMIPT.YUPI_STG_TERMINALS (
    TERMINAL_ID VARCHAR2 ( 20 BYTE ),
    TERMINAL_TYPE CHAR ( 3 BYTE ),
    TERMINAL_CITY VARCHAR2 ( 50 BYTE ),
    TERMINAL_ADDRESS VARCHAR2( 100 BYTE ),
    CREATE_DT DATE,
    UPDATE_DT DATE
);
CREATE TABLE DEMIPT.YUPI_STG_PASSPORT_BLACKLIST (	 
	PASSPORT_NUM VARCHAR2( 15 BYTE ), 
	ENTRY_DT DATE   
);
CREATE TABLE DEMIPT.YUPI_STG_CARDS (	
    CARD_NUM CHAR( 20 BYTE ), 
	ACCOUNT_NUM CHAR( 20 BYTE ),
    CREATE_DT DATE, 
	UPDATE_DT DATE
);
CREATE TABLE DEMIPT.YUPI_STG_ACCOUNTS (	
    ACCOUNT CHAR( 20 BYTE ), 
	VALID_TO DATE, 
	CLIENT VARCHAR2( 20 BYTE ),
    CREATE_DT DATE, 
	UPDATE_DT DATE 
);
CREATE TABLE DEMIPT.YUPI_STG_CLIENTS (	
    CLIENT_ID VARCHAR2( 20 BYTE ), 
	LAST_NAME VARCHAR2( 100 BYTE ), 
	FIRST_NAME VARCHAR2( 100 BYTE ), 
	PATRONYMIC VARCHAR2( 100 BYTE ),  
	DATE_OF_BIRTH DATE,
    PASSPORT_NUM VARCHAR2( 15 CHAR ),
    PASSPORT_VALID_TO DATE,
    PHONE VARCHAR2( 20 BYTE ),
    CREATE_DT DATE, 
	UPDATE_DT DATE 
)