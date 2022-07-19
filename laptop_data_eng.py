import pandas as pd

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

laptop_df['processor_brand'].value_counts()
laptop_df['processor_gnrtn'].value_counts()
laptop_df['processor'].value_counts()
laptop_df['ram'].value_counts()
laptop_df['model'].value_counts()

# rating 변수는 별점 횟수이며 star_rating 은 평균 별점으로 예측
# rating 변수가 없는 값은 star_rating도 없다. 이는 리뷰도 동일
# rating 변수를 판매량을 보여주는 지표로 생각해도 괜찮지 않을까
# 따라서 나머지 변수와 rating 과 관련된 정보를 분석해서 모델을 만들어 본다.
