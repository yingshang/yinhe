from django.shortcuts import render
from django.http import HttpResponse
from mitmproxy import flow, proxy, controller, options
from mitmproxy.proxy.server import ProxyServer
from scan.proxy import WSProxy
from scan.sqlinjection import autosqli
from celery.decorators import task
from scan.models import filter_data,proxy_data
from scan.sqlinjection import inject_data
#set proxy capture data


def capture(request):
    port = request.GET.get('port',8888)  #
    mode = request.GET.get('mode','regular')  #mode=regular
    opts = options.Options(
        listen_port=int(port),
        mode=mode,
        cadir="./ssl/",
    )
    unsave_data = False
    config = proxy.ProxyConfig(opts)
    state = flow.State()
    server = ProxyServer(config)
    m = WSProxy(opts, server, state, unsave_data)
    m.run()


def start_scan(request):
    scan()
    return HttpResponse('start scan')



@task
def scan():
    sqli = autosqli()
    sqli.start_scan()

@task
def scan_status():
    status = autosqli()
    status.data_scan()

def index(request):
    datas = inject_data.objects.all()
    return  render(request,'index.html',locals())

def display_data(request):
    datas = proxy_data.objects.all()
    return render(request, 'display_data.html', locals())

