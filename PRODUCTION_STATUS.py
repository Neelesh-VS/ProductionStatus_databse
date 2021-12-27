import mysql.connector
from hashlib import md5
from time import time
import string
import random
import time
import calendar
from datetime import datetime

conn = mysql.connector.connect(user='root', password='1234', host='127.0.0.1', port=3306, database='mydatabase', auth_plugin='mysql_native_password')

cursor = conn.cursor()

sql ='''CREATE TABLE IF NOT EXISTS CELL(
   CELL_ID INT AUTO_INCREMENT PRIMARY KEY,
   BARCODE BIGINT(10),
   DATE_TIME TIMESTAMP NOT NULL
)'''
cursor.execute(sql)
sql ='''CREATE TABLE IF NOT EXISTS PRODUCTION_STATUS(
   DATE_TIME BIGINT,
   CELL_ID INT,
   STATION_ID INT NOT NULL,
   PRODUCT_ID INT,
   BARCODE_ID VARCHAR(12),
   SERIAL_NUMBER VARCHAR(20),
   Revision_ID VARCHAR(10),
   Sachnummer VARCHAR(50),
   AQ_Typ VARCHAR(10),
   VENDOR_ID INT,
   MF_SPECIFICATION VARCHAR(20),
   MF_STATUS INT,
   INDEX ID(CELL_ID,STATION_ID,PRODUCT_ID)
)
PARTITION BY RANGE (DATE_TIME)(
PARTITION P0 VALUES LESS THAN(1642319037),
PARTITION P1 VALUES LESS THAN(1642981915),
PARTITION P2 VALUES LESS THAN(1643732061),
PARTITION P3 VALUES LESS THAN(1644202208),
PARTITION P4 VALUES LESS THAN(1644903410),
PARTITION P5 VALUES LESS THAN MAXVALUE
)'''
cursor.execute(sql)

date_time=[]
station_id=[]
cell_id=[]
product_id=[]
barcode_id=[]
serial=[]
revision_id=[]
sachnummer=[]
vendor=[]
aq_type=[]
spec=[]
status=[]
param_list=[]



start_time = int(time.time())
end_time = start_time + 5184000
for j in range(50):
    for i in range(0,20000):
        N=10
        m=6
        cell_id.append(str(random.randint(1,5)))
        station_id.append(str(random.randint(1,20)))
        product_id.append(str(random.randint(1,200)))
        vendor.append(str(random.randint(1,2)))
        status.append(str(random.randint(0,5)))
        date_time.append(str(random.randint(start_time, end_time)))
        sachnummer.append(''.join(random.choices(string.digits, k=N)))
        aq_type.append(''.join(random.choices(string.ascii_uppercase+string.digits, k=m)))
        spec.append('.'.join(random.choices(string.digits, k=m)))
        barcode_id.append(''.join(random.choices(string.digits, k=N)))
        revision_id.append(''.join(random.choices(string.digits, k=m)))
        serial.append(''.join(random.choices(string.digits, k=N)))
        param_list.append(''.join(date_time+station_id+cell_id+product_id+barcode_id+serial+revision_id+sachnummer+aq_type+vendor+spec+status))
                      

    sql = "INSERT INTO PRODUCTION_STATUS(DATE_TIME,CELL_ID,STATION_ID,PRODUCT_ID,BARCODE_ID,SERIAL_NUMBER,Revision_ID,Sachnummer,AQ_Typ,VENDOR_ID,MF_SPECIFICATION,MF_STATUS) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cnt=0
    for param in param_list:
        values = (date_time[cnt],cell_id[cnt],station_id[cnt],product_id[cnt],barcode_id[cnt],serial[cnt],revision_id[cnt],sachnummer[cnt],aq_type[cnt],vendor[cnt],spec[cnt],status[cnt])
        cursor.execute(sql, values)
        cnt+=1
    conn.commit()
    print(len(param_list))
    del date_time[:],station_id[:],cell_id[:],product_id[:],barcode_id[:],serial[:],revision_id[:],sachnummer[:],vendor[:],aq_type[:],spec[:],status[:],param_list[:]

conn.close()
    




    
