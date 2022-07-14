import pymysql
import pandas as pd
import plotly.graph_objects as go
import plotly as py
from plotly.offline import init_notebook_mode
import os



db_server_IP = '127.0.0.1'
db_UserName = 'root'
db_PassWord = '123456'
charSet = 'utf8'

db = pymysql.connect(host=db_server_IP, user=db_UserName, password=db_PassWord, db='laptop_db', charset=charSet)
cursor = db.cursor()

sql = "SELECT * FROM laptop_data"

cursor.execute(sql)
database = cursor.fetchall()

data = list(database)
laptop_df = pd.DataFrame(data,columns=["ranking","title","maker","brand","price"])

pd.set_option("display.max_columns",None)
pd.options.display.float_format = '{:.2f}'.format

# 84번째 데이터의 경우 노트북을 대여해주는 상품으로 제외 한다.
laptop_df = laptop_df[laptop_df.loc[:,'maker'] != ""]
laptop_df.reset_index(drop=True,inplace=True)

init_notebook_mode()

labels = laptop_df['maker'].value_counts().index
values = laptop_df['maker'].value_counts().values

fig = go.Figure()
fig.add_trace(
    go.Pie(labels = labels , values = values)
)

fig.show()

if not os.path.exists("images"):
    os.mkdir("images")

fig.write_image("images/pie_chart.png")

db.close()