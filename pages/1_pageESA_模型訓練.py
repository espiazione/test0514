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
st.title("🌍  期末報告中彰沿海一帶差異")
st.write("LANDSAT/LT05/C02/T1_L2&LANDSAT/LE07/C02/T1_L2")

# 地理區域
my_point = ee.Geometry.Point([120.3356, 24.0494, 120.5795, 24.3223])

taichung = ee.Geometry.Rectangle([120.3356, 24.0494, 120.5795, 24.3223])

dataset = ee.ImageCollection('LANDSAT/LT05/C02/T1_L2').filterDate('1984-01-01', '1984-12-31').filterBounds(taichung)


# Applies scaling factors.
def apply_scale_factors(image):
  optical_bands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
  thermal_bands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
  return image.addBands(optical_bands, None, True).addBands(thermal_bands, None, True)

dataset = dataset.map(apply_scale_factors)
#變1張影像
dataset = dataset.median()


def addNDWI(image):
  ndwi = image.normalizedDifference(['SR_B2', 'SR_B4']).rename('ndwi')
  return image.addBands(ndwi)
withNdwi = addNDWI(dataset)
ndwiVis = {
  'min': -1.0,
  'max': 1.0,
  'palette': ['brown', 'beige', 'blue'],
  'bands': ['ndwi'],
}

m = geemap.Map()
m.set_center(120.9, 24.2, 10)
m.add_layer(withNdwi.select('ndwi').unmask(0).clip(taichung), ndwiVis, 'NDWI taichung 1984')

# 顯示地圖
my_Map.to_streamlit(height=600)

