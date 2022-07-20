import os

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode

# I used a kaggle laptop data
# From https://www.kaggle.com/datasets/kuchhbhi/2022-march-laptop-data


pd.set_option("display.max_columns", None)
pd.options.display.float_format = '{:.2f}'.format

raw_data = pd.read_csv("laptop_data/Cleaned_Laptop_data.csv")

raw_data[raw_data["processor_name"].isnull()]
display_zero = raw_data[raw_data["display_size"] == "0"]

# display_size 가 0 인 데이터 들은 ram 데이터도 없다.
# processor_name 이 없는 데이터도 포함한다.
display_zero[display_zero["ram_gb"].isnull()].count()
raw_data[raw_data["ram_gb"].isnull()].count()

# ssd와 hdd 가 0 인 데이터 들은 display_size 데이터도 없다.
ssd_hdd_zero = raw_data[(raw_data["ssd"] == 0) & (raw_data["hdd"] == 0)]
ssd_hdd_zero[ssd_hdd_zero["display_size"] == "0"].count()

# 따라서 ssd와 hdd 데이터가 0 인 데이터를 삭제하면 nan 데이터들이 제거된다.
laptop_df = raw_data[(raw_data["ssd"] != 0) | (raw_data["hdd"] != 0)]

# 칩셋 브랜드가 단 하나인 제품과 display_size 가 6th로 특이한 값은 같은 변수로 제거한다
laptop_df[laptop_df["processor_brand"] == "Pre-installed"]
laptop_df[laptop_df["display_size"] == "6th"]

laptop_df = laptop_df[laptop_df["display_size"] != "6th"]
laptop_df.reset_index(inplace=True, drop=True)

# display_size 를 반올림하여 변수의 갯수를 줄인다
laptop_df['display_size'] = laptop_df['display_size'].astype(float)
laptop_df['display_size'] = laptop_df['display_size'].round()
laptop_df['display_size'] = laptop_df['display_size'].astype(int)

# processor_name 과 processor_gnrtn 을 하나의변수로 만들기
# ram_gb 와 ram_type 데이터를 하나의 변수로 만들기
# 브랜드도 합쳐서 하나의 변수를 만들었을때 ryzen 칩셋을 쓰지만 브랜드가 intel 로 저장된 변수 확인 후 수정

laptop_df.loc[
    (laptop_df["processor_brand"] == "Intel") & (laptop_df["processor_name"] == "Ryzen 7"), "processor_brand"] = "AMD"

for i in range(len(laptop_df)):
    if laptop_df.loc[i, "processor_gnrtn"] == "Missing":
        laptop_df.loc[i, "processor"] = laptop_df.loc[i, "processor_brand"] + " " + laptop_df.loc[i, "processor_name"]
    else:
        laptop_df.loc[i, "processor"] = laptop_df.loc[i, "processor_brand"] + " " + laptop_df.loc[
            i, "processor_gnrtn"] + " " + laptop_df.loc[i, "processor_name"]
    laptop_df.loc[i, "ram"] = laptop_df.loc[i, "ram_type"] + " " + laptop_df.loc[i, "ram_gb"] + "GB"

# 파생변수를 만든 원래의 변수 삭제
# model 변수는 나머지 스펙을 요약하여 특정한 하나의 명칭으로 부르는 것을 의미한다고 판단하고 삭제 해도 상관없다고 생각해서 삭제한다
# reviews 변수또한 rating 과 star_rating 이 대신할수 있다고 생각해서 삭제한다

laptop_df.drop(
    columns=["model", "processor_brand", "processor_name", "processor_gnrtn", "ram_type", "ram_gb", "reviews"],
    inplace=True)

# rating 변수는 별점 횟수이며 star_rating 은 평균 별점으로 예측
# rating 변수가 없는 값은 star_rating도 없다. 이는 리뷰도 동일
# 따라서 나머지 변수와 rating 과 관련된 정보를 분석해서 모델을 만들어 본다.
# rating 변수를 확인하면 0인 값이 상당히 많고 중앙값이 17 이며 제 3 사분위수는 143 이다.
# 이를 이용하여 rating > 100 인 값을 good_item 변수로 만들어서 분류 모델을 만들어 학습한다.
# brand ram processor 중 value_count < 10 인 값은 etc로 저장한다.
for i in range(len(laptop_df)):
    if laptop_df.loc[i, "ratings"] >= 100:
        laptop_df.loc[i, "good_item"] = 1
    else:
        laptop_df.loc[i, "good_item"] = 0
    if laptop_df['brand'].value_counts()[laptop_df.loc[i, "brand"]] < 10:
        laptop_df.loc[i, "brand_eng"] = "etc"
    else:
        laptop_df.loc[i, "brand_eng"] = laptop_df.loc[i, "brand"]
    if laptop_df['processor'].value_counts()[laptop_df.loc[i, "processor"]] < 10:
        laptop_df.loc[i, "processor_eng"] = "etc"
    else:
        laptop_df.loc[i, "processor_eng"] = laptop_df.loc[i, "processor"]
    if laptop_df['ram'].value_counts()[laptop_df.loc[i, "ram"]] < 10:
        laptop_df.loc[i, "ram_eng"] = "etc"
    else:
        laptop_df.loc[i, "ram_eng"] = laptop_df.loc[i, "ram"]

laptop_df['good_item'] = laptop_df['good_item'].astype(int)

# 문자열로 이루어진 변수들과 rating의 상관관계를 알기 힘들기 때문에 문자열로 이루어진 변수를 더미 변수화 해준다.
# 각 변수별로 너무 적은 value_count를 가지는 값은 하나로 합친다
# os weight touchscreen msofiice
# old price는 latest_price 와 discount 로 설명할수 있다고 판단하고 삭제한다


laptop_df['processor_eng'].value_counts()
laptop_df['brand_eng'].value_counts()
laptop_df['ram_eng'].value_counts()
laptop_df['os'].value_counts()
laptop_df['os_bit'].value_counts()
laptop_df['graphic_card_gb'].value_counts()
laptop_df['weight'].value_counts()
laptop_df.info()

if not os.path.exists("kaggle_images"):
    os.mkdir("kaggle_images")

init_notebook_mode()

fig = go.Figure()
fig.add_trace(
    go.Heatmap(z=laptop_df.corr().values.tolist(),
               x=laptop_df.corr().columns.tolist(),
               y=laptop_df.corr().columns.tolist(),
               colorscale="Reds"
               )
)
fig.update_layout(
    {
        "title": {
            "text": "Heatmap from laptop_df (22.07.14)",
            "font": {
                "size": 14
            }
        }
    }
)

fig.write_image("kaggle_images/heatmap_chart.png")
