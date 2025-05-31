import streamlit as st
from datetime import date

st.set_page_config(layout="wide", page_title="彰化台中沿海發展變化")

st.title("應用程式主頁")

st.title("利用擴充器示範")



with st.expander("播放mp4檔"):
    video_file = open("dowload\ndwi_timelapse.mp4", "rb")  # "rb"指的是讀取二進位檔案（圖片、影片）
    video_bytes = video_file.read()
    st.video(video_bytes)
