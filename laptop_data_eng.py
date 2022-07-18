import pandas as pd

# I used a kaggle laptop data
# From https://www.kaggle.com/datasets/kuchhbhi/2022-march-laptop-data


pd.set_option("display.max_columns", None)
pd.options.display.float_format = '{:.2f}'.format

laptop_data = pd.read_csv("laptop_data/Cleaned_Laptop_data.csv")

laptop_data[laptop_data["processor_name"].isnull()]
acer_df = laptop_data[laptop_data["brand"] == "acer"]
display_zero = laptop_data[laptop_data["display_size"] == "0"]
laptop_data[(laptop_data["ssd"] == 0) & (laptop_data["hdd"] == 0)].count()

# display_size 가 0 인 데이터 들은 ram 데이터도 없다.
# processor_name 이 없는 데이터도 포함한다.
display_zero[display_zero["ram_gb"].isnull()].count()
laptop_data[laptop_data["ram_gb"].isnull()].count()

# ssd와 hdd 가 0 인 데이터 들은 display_size 데이터도 없다.
ssd_hdd_zero = laptop_data[(laptop_data["ssd"] == 0) & (laptop_data["hdd"] == 0)]
ssd_hdd_zero[ssd_hdd_zero["display_size"] == "0"].count()

# 따라서 ssd와 hdd 데이터가 0 인 데이터를 삭제하면 nan 데이터들이 제거된다.
laptop_df = laptop_data[(laptop_data["ssd"] != 0)|(laptop_data["hdd"] != 0)]


laptop_df['processor_brand'].value_counts()
laptop_data['processor_brand'].value_counts()
laptop_df['display_size'].value_counts()

laptop_df[laptop_df["processor_brand"]=="Pre-installed"]
laptop_df[laptop_df["display_size"]=="6th"]


# processor_name 과 processor_gnrtn 을 하나의변수로 만들기
# ram_gb 와 ram_type 데이터를 하나의 변수로 만들기
# 다른 정보를 이용하여 알수 없는 nan 데이터 삭제
