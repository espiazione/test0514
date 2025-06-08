import streamlit as st
from datetime import date

st.set_page_config(layout="wide", page_title="彰化台中沿海發展變化")

st.title("應用程式主頁")

st.title("利用擴充器示範")

markdown = """
這是1984年到2024年台中及彰化沿海一帶工業區發展變化影片。以NDWI的形式呈現。
從中可發現彰濱工業區大約是在1979年開始進行填海造陸的作業，並於2000年前後基本雛型完工，在2020年開始又進行新一波的工程。
而在台中港區則約在1983年逐步動工完成，並於1990年展開一系列增建計畫。

"""

st.markdown(markdown)

with st.expander("播放mp4檔"):
    video_file = open("ndwi_timelapse.mp4", "rb")
    video_bytes = video_file.read()

    # 用 Columns 來控制畫面寬度（左右留白）
    col1, col2, col3 = st.columns([1, 4, 1])  # 中間占比 4，左右各占 1

    with col2:
        st.video(video_bytes)  # 影片放中間、寬一點
