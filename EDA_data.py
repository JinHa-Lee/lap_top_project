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

# 가격이 너무 낮은 상품의 경우 노트북을 대여해주는 상품으로 제외 한다.
laptop_df = laptop_df[laptop_df.loc[:,'price'] >= 100000]
laptop_df.reset_index(drop=True,inplace=True)

init_notebook_mode()

if not os.path.exists("images"):
    os.mkdir("images")

labels = laptop_df['maker'].value_counts().index
values = laptop_df['maker'].value_counts().values


fig = go.Figure()
fig.add_trace(
    go.Pie(labels = labels , values = values)
)
fig.update_layout(
    {
        "title" : {
            "text" : "Laptop top 100 maker count (22.07.14)",
            "font" : {
                "size" : 14
            }
        }
    }
)

fig.write_image("images/pie_chart.png")


fig = go.Figure()
fig.add_trace(
    go.Bar(x = laptop_df['ranking'], y = laptop_df['price'])
)
fig.update_layout(
    {
        "title" : {
            "text" : "Laptop price by ranking (22.07.14)",
            "font" : {
                "size" : 14
            }
        }
    }
)

fig.write_image("images/bar_chart.png")

laptop_group = laptop_df.groupby('maker').mean()


fig = go.Figure()
fig.add_trace(
    go.Bar(x = laptop_group.index , y = laptop_group['price'], text = laptop_group['price'].round(), textposition= "outside")
)

fig.update_layout(
    {
        "title" : {
            "text" : "Average price by maker (22.07.14)",
            "font" : {
                "size" : 14
            }
        }
    }
)

fig.write_image("images/average_price_chart.png")

laptop_df_top10 = laptop_df[laptop_df["ranking"]<=30]

labels = laptop_df_top10['maker'].value_counts().index
values = laptop_df_top10['maker'].value_counts().values


fig = go.Figure()
fig.add_trace(
    go.Pie(labels = labels , values = values)
)
fig.update_layout(
    {
        "title" : {
            "text" : "Laptop top 30 maker count (22.07.14)",
            "font" : {
                "size" : 14
            }
        }
    }
)

fig.write_image("images/top_30_pie_chart.png")

db.close()