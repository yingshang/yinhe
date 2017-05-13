# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required   #auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from forms import *
from models import UserInfo
import json
from result import wyproxy_request_handle,wyproxy_response_handle
import time
from scan.tasks import scan
from django.http.response import HttpResponse, HttpResponseRedirect
from mitmproxy import flow, proxy, controller, options
from mitmproxy.proxy.server import ProxyServer
# Create your views here.
#@csrf_exempt

class WYProxy(flow.FlowMaster):
    def __init__(self, opts, server, state, unsave_data):
        super(WYProxy, self).__init__(opts, server, state)
        self.unsave_data = unsave_data

    def run(self):
        try:
            print("start")
            flow.FlowMaster.run(self)
            
        except KeyboardInterrupt:
            self.shutdown()
    @controller.handler
    def request(self, f):
        wyproxy_request_handle(f)

    @controller.handler
    def response(self, f):
        
        wyproxy_response_handle(f)
        #parser = ResponseParser(f)
        #insert_result(parser.parser_data())
        
    
   

def login(request):                   #登陆view
    if request.method == 'POST':
        form = userinfo(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            status = UserInfo.objects.filter(username__exact = username,password__exact = password)
            if status:
                return HttpResponse("scess")
            else:
                return HttpResponseRedirect('/login')
    else:
        form = userinfo()
    return render(request,'login.html',{'form':form})


def capture(request):
    if request.method == 'POST':
        capture_form = cap(request.POST)
        if capture_form.is_valid():
            mode = capture_form.cleaned_data['mode']
            port = capture_form.cleaned_data['port']
            opts = options.Options(
            listen_port=int(port),
            mode=mode,
            cadir="./ssl/",
                )
            unsave_data = False
            config = proxy.ProxyConfig(opts)
            state = flow.State()
            server = ProxyServer(config)
            m = WYProxy(opts, server, state, unsave_data)
            m.run()
            return HttpResponse("123")
        
    else:
        capture_form = cap()
    return render(request,'capture.html',{'capture_form':capture_form})


@login_required
def getScan(request):
    data = []
    host = request.POST['host']
    #arguments = request.POST['arguments']
    port = request.POST['port']
    scan(host,port)
    return JsonResponse(data,safe=False)
