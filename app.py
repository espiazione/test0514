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
st.title("🌍 使用服務帳戶連接 GEE 的 Streamlit App")#標題


# 地理區域
point = ee.Geometry.Point([121.56, 25.03])

# 擷取 無雲
image = (
    ee.ImageCollection('COPERNICUS/S2_HARMONIZED')
    .filterBounds(point)
    .filterDate('2021-01-01', '2022-01-01')
    .sort('CLOUDY_PIXEL_PERCENTAGE')
    .first()
    .select('B.*')
)
vis_params = {'min':100, 'max': 3500,  'bands': ['B8', 'B4', 'B3']}
result001 = image

Map = geemap.Map()
Map.centerObject(result001, 8)
Map.addLayer(result001.randomVisualizer(), {}, 'K-Means clusters')
Map.centerObject(image, 8)
Map.addLayer(image, vis_params, 'Sentinel-2 flase color')

training001 = image.sample(
    **{
        'region': image.geometry(),  # 若不指定，則預設為影像image的幾何範圍。
        'scale': 10,
        'numPixels': 10000,
        'seed': 0,
        'geometries': True,  # 設為False表示取樣輸出的點將忽略其幾何屬性(即所屬網格的中心點)，無法作為圖層顯示，可節省記憶體。
    }
)
Map.addLayer(training001, {}, 'Training samples')
n_clusters = 10
clusterer_KMeans = ee.Clusterer.wekaKMeans(nClusters=n_clusters).train(training001)
result002 = image.cluster(clusterer_KMeans)

Map = geemap.Map()
Map.centerObject(result001, 8)
Map.addLayer(result001.randomVisualizer(), {}, 'K-Means clusters')

legend_dict = {
    'zero': '#ab0000',
    'one': '#1c5f2c',
    'two': '#d99282',
    'three': '#466b9f',
    'four': '#ab6c28',
     'five': '#ff0004',
    'six': '#868686',
    'seven': '#10d22c',
}
# 為分好的每一群賦予標籤

palette = list(legend_dict.values())
vis_params_001 = {'min': 0, 'max': 7, 'palette': palette}


Map.centerObject(result001, 8)
Map.addLayer(result001, vis_params_001, 'Labelled clusters')
Map.add_legend(title='Land Cover Type', legend_dict = legend_dict, position = 'bottomright')
Map = geemap.Map()

left_layer = geemap.ee_tile_layer(result001 .randomVisualizer(), {}, 'wekaKMeans clustered land cover')
right_layer = geemap.ee_tile_layer(result002 .randomVisualizer(), {}, 'wekaXMeans classified land cover')

Map.centerObject(image.geometry(), 9)
Map.split_map(left_layer, right_layer)

Map.to_streamlit(height=600)
