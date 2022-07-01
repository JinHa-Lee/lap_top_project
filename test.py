import pymysql

import crawling_data
import make_sql_database


make_sql_database.create_db("laptop_db")

create_table ="""
CREATE TABLE laptop_data (
RANKING INT NOT NULL PRIMARY KEY,
TITLE VARCHAR(100) NOT NULL,
MAKER VARCHAR(50),
BRAND VARCHAR(50),
LOWEST_PRICE INT
);
"""

make_sql_database.create_table("laptop_db", 'laptop_data', create_table)

item_data = crawling_data.naver_api_crawling()


db_server_IP = '127.0.0.1'
db_UserName = 'root'
db_PassWord = '123456'
charSet = 'utf8'

db = pymysql.connect(host=db_server_IP, user=db_UserName, password=db_PassWord, db='laptop_db', charset=charSet)
cursor = db.cursor()

ranking = 0
for item in item_data['items']:
    ranking += 1
    cursor.execute("INSERT INTO laptop_data (RANKING, TITLE, MAKER, BRAND,LOWEST_PRICE) VALUES ('"+str(ranking)+"','"+item['title'].replace("<b>","").replace("</b>","")+"','"+item['maker']+"','"+item['brand']+"','"+str(item['lprice'])+"')")

db.commit()
db.close()
