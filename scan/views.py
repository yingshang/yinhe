# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required   #auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from forms import *
from models import UserInfo,Result
import json
from result import wyproxy_request_handle,wyproxy_response_handle
from autosqlmap import autosqli
from scan.tasks import scan
from django.http.response import HttpResponse, HttpResponseRedirect
from mitmproxy import flow, proxy, controller, options
from mitmproxy.proxy.server import ProxyServer
import os
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

def run(request):
    inject = autosqli()
    inject.new_taskid()
    inject.start_scan()
    pass
def capture_data(request):
    results = Result.objects.all()
    print results
    return render_to_response("capture_data.html",locals())
def detail_data(request):
    results = Result.objects.all()
    return render_to_response("detail_data.html",locals())

def del_data(request,id):
    delete = Result.objects.get(id=id).delete()
    results = Result.objects.all()
    return render_to_response("capture_data.html",locals())

def flush_data(request):
    flush = Result.objects.all().delete()
    return render_to_response("capture_data.html",locals())
def sqli(request,taskid):
    data = autosqli(taskid=taskid)
    status = data.data_scan()
    
    return render_to_response("sqli.html",locals())
def sqli_detail(request,taskid):
    data = autosqli(taskid=taskid)
    status = data.sqli_detail()
    return render_to_response("sqli_detail.html",locals())

#@login_required
@csrf_exempt
def getScan(request):
    if request.method == 'POST':
        form = nm(request.POST)
        if form.is_valid():
            host= form.cleaned_data['host']
            port = form.cleaned_data['port']        
            data = scan(host,port)
    else:
        form = nm()
    return render_to_response("nmap.html",locals())