import streamlit as st
import ee
from google.oauth2 import service_account
import geemap.foliumap as geemap

# 從 Streamlit Secrets 讀取 GEE 服務帳戶金鑰 JSON
service_account_info = st.secrets["GEE_SERVICE_ACCOUNT"]

# 使用 google-auth 進行 GEE 授權
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)

# 初始化 GEE
ee.Initialize(credentials)

###############################################

st.set_page_config(layout="wide")
st.title("🌍  期末作業：GEE Streamlit App 練習")
st.write("Harmonized Sentinel-2 MSI: MultiSpectral Instrument, Level-1C ESA_WorldCover2021")

# 地理區域
my_point = ee.Geometry.Point([121.462129, 25.108993])

# 擷取 Harmonized Sentinel-2 MSI: MultiSpectral Instrument, Level-1C 衛星影像
my_image = (
    ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
    .filterBounds(my_point)
    .filterDate('2020-01-01', '2021-01-01')
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first()
    .select('B.*')
)

vis_params = {'min':100, 'max': 3500, 'bands': ['B8',  'B4',  'B3']}

my_lc = ee.Image('ESA/WorldCover/v100/2020')
# ESA WorldCover 10m v200
# https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100#bands

classValues = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]
remapValues = ee.List.sequence(0, 10)
label = 'lc'
my_lc = my_lc.remap(classValues, remapValues, bandName='Map').rename(label).toByte()#把剛剛的數列0~10儲存格式變8位元

classVis = {
  'min': 0,
  'max': 10,
  'palette': ['006400' ,'ffbb22', 'ffff4c', 'f096ff', 'fa0000', 'b4b4b4',
            'f0f0f0', '0064c8', '0096a0', '00cf75', 'fae6a0']
}

# 顯示地圖
# 建立地圖物件（不傳入任何參數）
# 建立地圖物件
my_Map = geemap.Map()

# 加入圖層
my_Map.addLayer(my_image, vis_params, 'Sentinel-2 Image')
my_Map.addLayer(my_lc, classVis, 'ESA WorldCover 10m v100')

# 設定地圖中心
my_Map.centerObject(my_image.geometry(), 10)

# 加入圖例（使用預設圖例）
my_Map.add_legend(title='ESA Land Cover Type', builtin_legend='ESA_WorldCover')

# 顯示地圖
my_Map.to_streamlit(height=600)

