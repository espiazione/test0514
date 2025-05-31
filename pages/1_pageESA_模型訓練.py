import streamlit as st
import folium 
import ee
from google.oauth2 import service_account
import geemap.foliumap as geemap

# ---------------------
# Streamlit 設定
# ---------------------
st.set_page_config(layout="wide")
st.title("🌍 中彰沿海 NDWI 比較（1984 vs 2024）")
st.write("資料來源：LANDSAT/LT05/C02/T1_L2 & LANDSAT/LC08/C02/T1_L2")

# ---------------------
# GEE 認證
# ---------------------
service_account_info = st.secrets["GEE_SERVICE_ACCOUNT"]
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)
ee.Initialize(credentials)

# ---------------------
# 區域定義
# ---------------------
taichung = ee.Geometry.Rectangle([120.3356, 24.0494, 120.5795, 24.3223])

# ---------------------
# 影像前處理函式
# ---------------------
def apply_scale_factors(image):
    optical_bands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
    thermal_bands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
    return image.addBands(optical_bands, None, True).addBands(thermal_bands, None, True)

def addNDWI_L5(image):
    ndwi = image.normalizedDifference(['SR_B2', 'SR_B4']).rename('ndwi')
    return image.addBands(ndwi)

def addNDWI_L8(image):
    ndwi = image.normalizedDifference(['SR_B3', 'SR_B5']).rename('ndwi')
    return image.addBands(ndwi)

# ---------------------
# 1984：Landsat 5
# ---------------------
image_1984 = (
    ee.ImageCollection('LANDSAT/LT05/C02/T1_L2')
    .filterDate('1984-01-01', '1984-12-31')
    .filterBounds(taichung)
    .map(apply_scale_factors)
    .median()
)
ndwi_1984 = addNDWI_L5(image_1984).select('ndwi').unmask(0).clip(taichung)

# ---------------------
# 2024：Landsat 8
# ---------------------
image_2024 = (
    ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
    .filterDate('2024-01-01', '2024-12-31')
    .filterBounds(taichung)
    .map(apply_scale_factors)
    .median()
)
ndwi_2024 = addNDWI_L8(image_2024).select('ndwi').unmask(0).clip(taichung)

# ---------------------
# NDWI 色彩視覺化參數
# ---------------------
ndwi_vis = {
    'min': -1.0,
    'max': 1.0,
    'palette': ['brown', 'beige', 'blue'],
}
legend_html = """
     <div style="
         position: fixed; 
         bottom: 30px; left: 30px; width: 200px; height: 120px; 
         background-color: white;
         border:2px solid grey;
         z-index:9999;
         font-size:14px;
         padding: 10px;
     ">
     <b>NDWI 色階說明</b><br>
     <i style="background: brown; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> 低水分 (裸地)<br>
     <i style="background: beige; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> 中水分 (植被/濕地)<br>
     <i style="background: blue; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> 高水分 (水體)<br>
     </div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

# ---------------------
# 建立比較地圖
# ---------------------
m = geemap.Map()
left_layer = geemap.ee_tile_layer(ndwi_1984, ndwi_vis, 'NDWI 1984')
right_layer = geemap.ee_tile_layer(ndwi_2024, ndwi_vis, 'NDWI 2024')

m.centerObject(taichung, 10)
m.split_map(left_layer, right_layer)
m.add_legend(title='NDWI 色階', legend_dict={
    '低水分 (裸地)': 'brown',
    '中水分 (濕地/植生)': 'beige',
    '高水分 (水域)': 'blue'
}, draggable=False, position='bottomright')

m.to_streamlit(height=600)


