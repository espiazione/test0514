import streamlit as st
import ee
from google.oauth2 import service_account
import geemap.foliumap as geemap

# GEE 認證
service_account_info = st.secrets["GEE_SERVICE_ACCOUNT"]
credentials = service_account.Credentials.from_service_account_info(
    service_account_info,
    scopes=["https://www.googleapis.com/auth/earthengine"]
)
ee.Initialize(credentials)

# Streamlit 設定
st.set_page_config(layout="wide")
st.title("🌍 使用服務帳戶連接 GEE 的 Streamlit App")

# 設定中心點為彰師大進德校區
point = ee.Geometry.Point([120.5583462887228, 24.081653403304525])

# 影像處理
image = (
    ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
    .filterBounds(point)
    .filterDate('2021-01-01', '2022-01-01')
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first()
    .select('B.*')
)

# 可見光參數（False color）
vis_params = {'min': 100, 'max': 3500, 'bands': ['B4', 'B3', 'B2']}

# 隨機取樣
training_samples = image.sample(
    region=image.geometry(),
    scale=10,
    numPixels=10000,
    seed=0,
    geometries=True
)

# 分群訓練
n_clusters = 10
clusterer = ee.Clusterer.wekaKMeans(nClusters=n_clusters).train(training_samples)
clustered_result = image.cluster(clusterer)

# 標籤與圖例設定
legend_dict = {
    'zero': '#ff0000',
    'one': '#00ff00',
    'two': '#0000ff',
    'three': '#ffff00',
    'four': '#00ffff',
    'five': '#ff00ff',
    'six': '#888888',
    'seven': '#ff8800',
    'eight': '#00ff88',
    'nine': '#8800ff',
}
palette = list(legend_dict.values())
vis_clustered = {'min': 0, 'max': 9, 'palette': palette}

# Split-map 顯示
Map = geemap.Map()
Map.centerObject(image.geometry(), 9)

left_layer = geemap.ee_tile_layer(image.visualize(**vis_params), {}, 'Sentinel-2 False Color')
right_layer = geemap.ee_tile_layer(clustered_result.visualize(**vis_clustered), {}, 'KMeans Clustering')

Map.split_map(left_layer, right_layer)
Map.add_legend(title='Land Cover Clusters', legend_dict=legend_dict, position='bottomright')

Map.to_streamlit(height=600)

