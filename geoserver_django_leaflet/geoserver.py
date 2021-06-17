# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import requests
base_url = 'http://localhost:8080/'
# 获取地图瓦片服务
def wmts(request):
    print(request)
    url = base_url+'geoserver/fangjia/wms?service=WMS&request=GetMap&layers='+request.GET['layers']+\
        '&styles=&format='+request.GET['format']+'&transparent='+request.GET['transparent']+\
          '&version='+request.GET['version']+'&width='+request.GET['width']+'&height='+request.GET['height']+\
          '&srs='+request.GET['srs']+'&bbox='+request.GET['bbox']
    if 'CQL_FILTER' in request.GET:
        url = url + '&CQL_FILTER=' + request.GET['CQL_FILTER']
    print(url)
    image_data = requests.get(url=url,stream=True)
    return HttpResponse(image_data,content_type='image/png')
# 访问tile_wmts页面
def tile_wmts(request):
    return render(request,'tile_wmts.html')
# 根据查询条件，获取要素服务
def getfeature(request):
    url = base_url + 'geoserver/wfs?request=GetFeature&version=1.1.0&typeName='+request.GET['typeName']+'&outputFormat=application%2Fjson'
    if 'BBOX' in request.GET:
        url = url + '&BBOX=' + request.GET['BBOX']
    if 'CQL_FILTER' in request.GET:
        url = url + '&CQL_FILTER=' + request.GET['CQL_FILTER']
    print(url)
    json_data = requests.get(url=url)
    return HttpResponse(json_data,content_type='application/json')
# 访问bbox_feature页面
def bbox_feature(request):
    return render(request,'bbox_feature.html')
# 访问attr_feature页面
def attr_feature(request):
    return render(request,'attr_feature.html')
# 渲染draw页面
def draw(request):
    return render(request, 'draw.html')
# 渲染delete页面
def remove(request):
    return render(request,'remove.html')

# 提交 gml到geoserver
def postgml(request):
    if request.POST:
        head = {"Content-Type": "text/xml; charset=UTF-8", "Connection": "close"}
        r = requests.post(base_url+'geoserver/wfs', data=request.POST['gml'].encode('gbk'), headers=head)
    return HttpResponse(r.text)



