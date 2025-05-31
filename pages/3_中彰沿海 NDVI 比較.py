import streamlit as st
import ee
from google.oauth2 import service_account
import geemap.foliumap as geemap
import folium

st.set_page_config(layout="wide")
st.title("🌿 中彰沿海 NDVI 比較（1984 vs 2024）")
st.write("資料來源：LANDSAT/LT05/C02/T1_L2 & LANDSAT/LC08/C02/T1_L2")

# GEE 認證
service_account_info = st.secrets["GEE_SERVICE_ACCOUNT"]
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)
ee.Initialize(credentials)

# 區域範圍
taichung = ee.Geometry.Rectangle([120.3356, 24.0494, 120.5795, 24.3223])

def apply_scale_factors(image):
    optical_bands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
    thermal_bands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
    return image.addBands(optical_bands, None, True).addBands(thermal_bands, None, True)

# 加入 NDVI 波段
def addNDVI(image, red_band, nir_band):
    ndvi = image.normalizedDifference([nir_band, red_band]).rename('ndvi')
    return image.addBands(ndvi)

image_1984 = (
    ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
    .filterDate('1984-01-01', '1984-12-31')
    .filterBounds(taichung)
    .map(apply_scale_factors)
    .median()
)
ndvi_1984 = addNDVI(image_1984, 'SR_B3', 'SR_B4').select('ndvi').unmask(0).clip(taichung)

image_2024 = (
    ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    .filterDate('2024-01-01', '2024-12-31')
    .filterBounds(taichung)
    .map(apply_scale_factors)
    .median()
)
ndvi_2024 = addNDVI(image_2024, 'SR_B4', 'SR_B5').select('ndvi').unmask(0).clip(taichung)

ndvi_vis = {
    'min': -1.0,
    'max': 1.0,
    'palette': ['#d73027', '#fdae61', '#a6d96a', '#1a9850'],  
}

# 建立地圖
m = geemap.Map()
left_layer = geemap.ee_tile_layer(ndvi_1984, ndvi_vis, 'NDVI 1984')
right_layer = geemap.ee_tile_layer(ndvi_2024, ndvi_vis, 'NDVI 2024')
m.centerObject(taichung, 10)
m.split_map(left_layer, right_layer)

# 圖例 HTML
legend_html = """
     <div style="
         position: fixed; 
         bottom: 30px; left: 30px; width: 220px; height: 130px; 
         background-color: white;
         border:2px solid grey;
         z-index:9999;
         font-size:14px;
         padding: 10px;
     ">
     <b>NDVI 色階說明</b><br>
     <i style="background:#d73027; width: 18px; height: 18px; float: left; margin-right: 8px;"></i> 無植生 (裸地)<br>
     <i style="background:#fdae61; width: 18px; height: 18px; float: left; margin-right: 8px;"></i> 草地/低度植被<br>
     <i style="background:#a6d96a; width: 18px; height: 18px; float: left; margin-right: 8px;"></i> 中等植被<br>
     <i style="background:#1a9850; width: 18px; height: 18px; float: left; margin-right: 8px;"></i> 濃密植被<br>
     </div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# 顯示地圖
m.to_streamlit(height=600)
