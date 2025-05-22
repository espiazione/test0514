import streamlit as st
from datetime import date

st.set_page_config(layout="wide", page_title="這是Streamlit App第二次練習！")

st.title("應用程式主頁")
#超連結方式
st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io), [GEE](https://earthengine.google.com/), 
    [geemap](https://leafmap.org) and [leafmap](https://leafmap.org). 
    """
)

st.header("Instructions")

markdown = """
1. You can use it as a template for your own project.
2. Customize the sidebar by changing the sidebar text and logo in each Python file.
3. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.

"""

st.markdown(markdown)







    
