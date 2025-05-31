import streamlit as st
from datetime import date

st.set_page_config(layout="wide", page_title="彰化台中沿海發展變化")

st.title("應用程式主頁")

st.title("利用擴充器示範")

markdown = """
1. You can use it as a template for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python file.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

"""

st.markdown(markdown)

with st.expander("播放mp4檔"):
    video_file = open("ndwi_timelapse.mp4", "rb")  # "rb"指的是讀取二進位檔案（圖片、影片）
    video_bytes = video_file.read()
    st.video(video_bytes)
