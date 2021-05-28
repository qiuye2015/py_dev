import pprint
import requests
import json
import math
# 太酷炫了，我用Python画出了北上广深的地铁路线动态图
url = 'http://map.amap.com/service/subway?_1615466846985&srhdata=1100_drw_beijing.json'
response = requests.get(url)
result = json.loads(response.text)
print(result)
stations = []
for i in result['l']:
    station = []
    for a in i['st']:
        station.append([float(b) for b in a['sl'].split(',')])
    stations.append(station)
# pprint.pprint(stations)

#需要的两个常量先设置好
pi = 3.1415926535897932384 #π
r_pi = pi * 3000.0/180.0

def gcj02_bd09(lon_gcj02,lat_gcj02):
    b = math.sqrt(lon_gcj02 * lon_gcj02 + lat_gcj02 * lat_gcj02) + 0.00002 * math.sin(lat_gcj02 * r_pi)
    o = math.atan2(lat_gcj02 , lon_gcj02) + 0.000003 * math.cos(lon_gcj02 * r_pi)
    lon_bd09 = b * math.cos(o) + 0.0065
    lat_bd09 = b * math.sin(o) + 0.006
    return [lon_bd09,lat_bd09]

result = []
for station in stations:
    result.append([gcj02_bd09(*point) for point in station])

pprint.pprint(result)

from pyecharts.charts import BMap
from pyecharts import options as opts
from pyecharts.globals import BMapType, ChartType

map_b = (
    BMap(init_opts = opts.InitOpts(width = "800px", height = "600px"))
    .add_schema(
        baidu_ak = '*****', #百度地图开发应用appkey
        center = [116.403963, 39.915119], #当前视角的中心点
        zoom = 10, #当前视角的缩放比例
        is_roam = True, #开启鼠标缩放和平移漫游
    )
    .add(
        series_name = "",
        type_ = ChartType.LINES, #设置Geo图类型
        data_pair = result, #数据项
        is_polyline = True, #是否是多段线，在画lines图情况下#
        linestyle_opts = opts.LineStyleOpts(color = "blue", opacity = 0.5, width = 1), # 线样式配置项
    )
    .add_control_panel(
        maptype_control_opts = opts.BMapTypeControlOpts(type_ = BMapType.MAPTYPE_CONTROL_DROPDOWN), #切换地图类型的控件
        scale_control_opts = opts.BMapScaleControlOpts(), #比例尺控件
        overview_map_opts = opts.BMapOverviewMapControlOpts(is_open = True), #添加缩略地图
        navigation_control_opts = opts.BMapNavigationControlOpts() #地图的平移缩放控件
    )
)

map_b.render(path = 'subway_beijing.html')