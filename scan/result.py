# -*- coding: utf-8 -*-
from models import Result
import json

static_file = ['.js','.txt','.mp3','.css','.jpg','.png','.gif','.woff','.ico','.pdf','.mp4','.svg']
def wyproxy_request_handle(flow):
    """wyproxy send data to server before processing"""
    

    # change the request headers['Host']
    # flow.request.headers['X-Online-Host'] = 'wap.gd.10086.cn'


def wyproxy_response_handle(flow):
    path = '/{}'.format('/'.join(flow.request.path_components)) 
    code =0 
    for i in static_file:                   #Exclude static file in capture packet
        if path.find(i)>0:
            code =1
            break
    
    if code == 0 :
        #print json.dump(flow.request.headers)
        if not Result.objects.filter(url=flow.request.url) and not Result.objects.filter(request_headers=flow.request.headers):
            Result.objects.create(             #save data in database
                          host = flow.request.host,
                          port = flow.request.port,
                          method = flow.request.method,
                          url = flow.request.url,
                          scheme = flow.request.scheme,
                          request_headers=flow.request.headers,
                            request_content = flow.request.content,
                            path = path,
                            status_code =flow.response.status_code,
                            response_headers = flow.response.headers,
                            response_content = flow.response.content,
                            request_cookies = flow.request.cookies,
                            http_version = flow.request.http_version
                                    )
           
 