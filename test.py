import pymysql

import crawling_data
import make_sql_database

# item_data = crawling_data.naver_api_crawling()

make_sql_database.create_db("laptop_db")

create_table ="""
CREATE TABLE laptop_data (
RANKING INT NOT NULL PRIMARY KEY,
TITLE VARCHAR(50) NOT NULL,
MAKER VARCHAR(20),
BRAND VARCHAR(20),
LOWEST_PRICE INT
);
"""

make_sql_database.create_table("laptop_db", 'laptop_data', create_table)

db_server_IP = '127.0.0.1'
db_UserName = 'root'
db_PassWord = '123456'
charSet = 'utf8'

db = pymysql.connect(host=db_server_IP, user=db_UserName, password=db_PassWord, charset=charSet)
cursor = db.cursor()

sqlQuery = "SHOW DATABASES"

cursor.execute(sqlQuery)

databaseList = cursor.fetchall()

for datatbase in databaseList:
    print(datatbase)
db.close()


db = pymysql.connect(host=db_server_IP, user=db_UserName, password=db_PassWord, db='laptop_db', charset=charSet)
cursor = db.cursor()

sqlQuery = "SHOW TABLES"

cursor.execute(sqlQuery)

tableList = cursor.fetchall()

for table in tableList:
    print(table)

db.close()
