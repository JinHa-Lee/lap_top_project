import pymysql

import make_sql_database

make_sql_database.create_db("test")

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
