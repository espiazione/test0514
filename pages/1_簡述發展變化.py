import streamlit as st
from datetime import date

st.set_page_config(layout="wide", page_title="彰化台中沿海發展變化")

st.title("應用程式主頁")

st.title("利用擴充器示範")

markdown = """
    這是1984年到2024年台中及彰化沿海一帶工業區發展變化影片。以NDWI的形式呈現。
    從中可發現彰濱工業區大約是在1995年開始進行填海造陸的作業，並於2001年左右完工。在2020年開始又進行新一波的工程。
而在台中沿海工業區則約在1987年動工，並於1994年大致完工。於1998年進行擴建。

"""

st.markdown(markdown)

with st.expander("播放mp4檔"):
    video_file = open("ndwi_timelapse.mp4", "rb")  # "rb"指的是讀取二進位檔案（圖片、影片）
    video_bytes = video_file.read()
    st.video(video_bytes)
