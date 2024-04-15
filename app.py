import streamlit as st
import pandas as pd
import openpyxl as xl
# import plotly
# from plotly import plotly.express as px
import plotly.express as px
# import plotly.express as px
# from datetime import datetime
# import iost
# from io import BytesIO
# import msoffcrypto
import matplotlib.pyplot as plt

df_all = pd.read_excel(
    # io = 'C:/Users/USER/anaconda3/envs/streamlit_test/visitor.xlsx',
    # io = 'C:/Users/USER/anaconda3/envs/streamlit_test/visitor.xlsx',
    io = 'visitor.xlsx',
    engine = 'openpyxl',
    # sheet_name = 'daily',
    sheet_name ='daily',
    skiprows = 1,
    usecols='a:i',
    nrows = 1500,
)
# https://stackoverflow.com/questions/21609781/why-call-git-branch-unset-upstream-to-fixup

# 컬럼명 chekc
print(df_all.columns.tolist()) 
# df = df_all.dropna(subset=['전시명'], how='any', axis=0)

# 컬럼명[전시명] 중 내용이 없는 행 제거
df = df_all.dropna(subset=['전시명'], how='any', axis=0)
print(df)
df['관람객k'] = df['관람객']/1000
#데이터 프레임 형식확인
df.info()

# 컬럼명(일자) 일자형식으로 변경

# df['일자'] = pd.to_datetime(df['일자'], format='%Y-%m-%d', errors='ignore')
# df['일자'] = pd.to_datetime(df['일자'], format='%Y-%m-%d %H:%M:%S', errors='raise')

#데이터 프레임 편집 - 일자 천단위 제거

# df['일자'] = df['일자'].str.replace(',','').astype(int)
# df_m.iloc[0] = df_m.iloc[0].str.replace(',','').astype(int)



#데이터 프레임 편집 - 관람객 천단위 넣기
# df['관람객'] = df['관람객'].apply(lambda int_num : '{:,}'.format(int_num))



#스트림릿

# 스트림릿 데이터프레임 참조
# https://docs.kanaries.net/ko/topics/Streamlit/streamlit-dataframe

#스트림릿용 df
S_df = df.astype({'년':'str','월':'str', '관람객':'int', '일자':'str','일차':'int', '무료':'str', '유료':'str'})

st.sidebar.header("Please Filter Here:")
전시 = st.sidebar.multiselect(
    "Select the 전시:",
    options=df["전시명"].unique(),
    default=df["전시명"].unique()
)



# 최신 전시일 확인 (윤협)
# df_MAX_D = df.loc[(df['전시명'] == '윤협') & (df['관람객'] > 0)]['일차'].transform('max')
df_MAX_D = df.loc[(df['전시명'] == '윤협') & (df['관람객'] > 0)]
print(df_MAX_D)
MAX_Day = df_MAX_D['일차'].max(axis=0)
st.title(MAX_Day)
df_MAX_D = df.loc[(df['전시명'] == '윤협') & (df['관람객'] > 0) & (df['관람객'] <= MAX_Day)]

S_df_selection = S_df.query(
    # "전시 == @city & Customer_type ==@customer_type & Gender == @gender"
    "전시명 == @전시"
)


st.title("test")
st.markdown("""
<style>
table {background-color: #f0f0f0;}
</style>
""", unsafe_allow_html=True)
# st.dataframe(df)
st.dataframe(S_df_selection.style.background_gradient(cmap='Blues'))



# print(MAX_Day)

# sales_by_hour[bar_chart]	

일차 = st.slider("전시일차선택 : ", 1,MAX_Day)

S_df_selection2 = S_df.query(
    # "전시 == @city & Customer_type ==@customer_type & Gender == @gender"
    "전시명 == @전시 & 일차 <= @일차"
)

visitor = S_df_selection2.groupby(by=["전시명"]).sum()[["관람객k"]].sort_values(by="관람객k")

전시별관람객 = px.bar(
visitor,
x=visitor.index,
y="관람객k",
title = "<b>전시별관람객</b>",
color_discrete_sequence=["#008388"] * len(visitor),
template="plotly_white",
# <style>
# .big-font {
text = "관람객k"
# text="관람객"/1000,

# }
# </style>
)

전시별관람객.update_layout(
    xaxis=(dict(tickmode="linear")),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False))
)
전시별관람객.update_layout(
font=dict(size=15))

st.plotly_chart(전시별관람객)

# 일차 = st.slider("전시일차선택 : ", 1,MAX_Day)



# # condition = (
# #     (tmp_df.tip < 1)&
# #     (tmp_df.color == 'yellow')&
# #     (tmp_df.fare >= 10)&
# #     (tmp_df.fare < 25)&
# #     (tmp_df.passengers > 1)&
# #     (tmp_df.pickup_borough == 'Manhattan')
# # )
# # 출처: https://csshark.tistory.com/63 [컴퓨터하는 상어:티스토리]