import streamlit as st
import pandas as pd

st.title("📊 子頁面：資料篩選")

# 檢查是否有日期資訊
if 'start_date' in st.session_state and 'end_date' in st.session_state:
    # 讀取資料
    df = pd.read_csv("sample_data.csv", parse_dates=['日期'])

    # 取得篩選條件
    start = st.session_state['start_date']
    end = st.session_state['end_date']

    # 篩選
    filtered_df = df[(df['日期'] >= pd.to_datetime(start)) & (df['日期'] <= pd.to_datetime(end))]

    st.write(f"你在*主頁*選擇的日期區間是：{start} 到 {end}")
    st.dataframe(filtered_df)
else:
    st.warning("請先回主頁選擇日期區間！")
