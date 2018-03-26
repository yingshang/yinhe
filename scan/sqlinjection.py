# coding: utf-8
from scan.models import proxy_data, filter_data, inject_data
import re
from django.http import JsonResponse
import os
import requests,json
from celery.decorators import task
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#过滤重复的数据包

@task
def filter():
    dates = proxy_data.objects.all()
    for date in dates:
        if date.method == 'GET':
            tmp = ''
            try:
                url = re.match('\S+\?', date.url).group()
                parms = date.url.split(url)[-1].split('&')
                for parm in parms:
                    tmp =  parm.split('=')[0]+ ','+tmp
                record = len(filter_data.objects.filter(url=date.url.split('?')[0]))
                if record != 0:
                    parm = filter_data.objects.get(url=date.url.split('?')[0]).parm
                    tmp_list = tmp.split(',')
                    parm_list = parm.split(',')
                    Union = list(set(tmp_list).union(set(parm_list))) #列表的并集
                    if len(Union) != len(parm_list):
                        packet = date.method + ' ' + date.url + ' ' + date.http_version + '\n' + date.request_headers
                        filter_data.objects.create(url=date.url,data_packet=packet,parm=tmp)
                else:
                    packet = date.method + ' ' + date.url + ' ' + date.http_version + '\n' + date.request_headers
                    filter_data.objects.create(
                        url=date.url.split('?')[0],
                        data_packet=packet,
                        parm=tmp)
            except AttributeError:
                pass

        elif date.method == 'POST':
            url = date.url
            record = len(filter_data.objects.filter(url=url))
            packet = date.method + ' ' + date.url + ' ' + date.http_version + '\n' + date.request_headers +'\n\n'+date.request_content
            post_data = date.request_content
            json_data = re.findall('^{\S+}$', post_data)
            if record ==0: #如果数据库没有记录，写入数据
                if len(date.request_content) >0: #post数据为0
                    if len(json_data) > 0:   #post为json方式
                        json_list = re.findall('"(.*?)":.*?,',json_data[0])
                        json_str = ",".join(json_list)
                        filter_data.objects.create(url=url,data_packet=packet,parm=json_str)
                    else: #post为正常方式，loginDate=2017-10-25&searchVal=&loginStatus=all&pageIndex=1&pageSize=10
                        parm = ''
                        parms = date.request_content.split('&')
                        for i in parms:
                            parm = i.split('=')[0]+','+parm
                        filter_data.objects.create(url=url,parm=parm,data_packet=packet)
                else:
                    filter_data.objects.create(url=url, parm='', data_packet=packet)
            else: #数据库有记录，如果记录重复，忽略
                if len(date.request_content) > 0:  # post数据为0
                    if len(json_data) > 0:   #post为json方式
                        json_list = re.findall('"(.*?)":.*?,',json_data[0])
                        data_list = filter_data.objects.filter(url=url)[0].parm.split(',')
                        Union = list(set(json_list).union(set(data_list)))  # 列表的并集
                        if len(Union) != len(data_list):
                            filter_data.objects.create(url=date.url, data_packet=packet, parm=",".join(json_list))

                    else: #post为正常方式，loginDate=2017-10-25&searchVal=&loginStatus=all&pageIndex=1&pageSize=10
                        parm = ''
                        print date.request_content
                        parms = date.request_content.split('&')
                        data_list = filter_data.objects.filter(url=url)[0].parm.split(',')
                        for i in parms:
                            parm = i.split('=')[0]+','+parm
                        parm_list = parm.split(',')
                        Union = list(set(parm_list).union(set(data_list)))  # 列表的并集
                        if len(Union) != len(data_list):
                            filter_data.objects.create(url=date.url, data_packet=packet, parm=parm)




class autosqli(object):
    def __init__(self, server='http://127.0.0.1:8775', taskid='', options={}):
        self.server = server
        self.options = options
        self.taskid = taskid
        self.headers = {'Content-Type': 'application/json'}
        self.data = ''

    def new_taskid(self):
        results = filter_data.objects.all()
        for result in results:
            if len(result.taskid) == 0:
                url = self.server + "/task/new"
                taskid = requests.get(url).json()['taskid']
                result.taskid = taskid
                result.save()
                try:
                    fp = open('taskid/' + taskid, 'w+')
                    fp.writelines(str(result.data_packet) + '\n')
                    fp.close()
                except UnicodeEncodeError :
                    pass



    def del_taskid(self):
        url = self.server + '/task/' + self.taskid + '/delete'

    def set_options(self):
        if self.options is None:
            return False
        else:
            url = self.server + "/option/" + self.taskid + "/set"
            data = json.dumps(self.options)
            responseData = requests.post(url, data=data, headers=self.header).json()['success']
            if responseData == True:
                return True
            else:
                return False

    def list_options(self):
        url = self.server + '/option/' + self.taskid + '/list'

    def get_options(self):
        url = self.server + '/option/' + self.taskid + '/get'

    def start_scan(self):
        self.new_taskid()
        results = filter_data.objects.all()
        for result in results:
            if result.status == '0':
                taskid = result.taskid
                inject_data.objects.create(taskid=taskid)
                payload = {
                        'requestFile': os.path.join(BASE_DIR, 'taskid') + '/' + taskid,
                        'level':3,
                           }
                url = self.server + "/scan/" + taskid + "/start"
                result.status='1'
                result.save()
                t = json.loads(requests.post(url, data=json.dumps(payload), headers=self.headers).text)


    def stop_scan(self):
        url = self.server + "/scan/" + self.taskid + "/stop"

    def status_scan(self):
        url = self.server + '/scan/' + self.taskid + '/status'

    def kill_scan(self):
        url = self.server + '/scan/' + self.taskid + '/kill'

    def data_scan(self):
        results = inject_data.objects.all()
        for result in results:
            url = self.server + '/scan/' + result.taskid + '/status'
            run_status = requests.get(url).json()['status']
            parameter = ''
            if run_status == 'terminated':
                if result.status == '0':
                    url = self.server + '/scan/' + result.taskid + '/data'
                    data = requests.get(url).json()['data']
                    if len(data) > 0 :
                        status = data[0]['status']
                        url1 = data[0]['value']['url']
                        for i in data[1]['value']:
                            dbms = i['dbms']
                            parameter = i['parameter'] +','+parameter
                        result.packet = filter_data.objects.get(taskid=result.taskid).data_packet
                        result.url =url1
                        result.dbms= dbms
                        result.vul_info = 'YES'
                        result.parameter = parameter
                        result.status = status
                        result.run_status = run_status
                        result.save()
                    else:
                        result.status = '1'
                        result.vul_info = 'NO'
                        result.run_status = run_status
                        result.save()
            elif run_status == 'running':
                result.run_status = run_status
                result.save()

