#-*-coding:utf-8-*-
import requests
import json
from models import Result,Sqlmap
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def list_all_dict(dict_a):
        if isinstance(dict_a,dict) : #使用isinstance检测数据类型
            for x in range(len(dict_a)):
                temp_key = dict_a.keys()[x]
                temp_value = dict_a[temp_key]
                print"%s : %s" %(temp_key,temp_value)
                list_all_dict(temp_value) #自我调用实现无限遍历
                
class autosqli(object):
    def __init__(self,server='http://127.0.0.1:8775',taskid ='',options={}):
        self.server = server
        self.options = options
        self.taskid = taskid
        
        self.headers = {'Content-Type': 'application/json'}
        self.data = ''
    def new_taskid(self):
        for id in Result.objects.all().values('id'):
            for i in Result.objects.filter(id=id['id']):
                url = self.server + "/task/new"
                taskid = requests.get(url).json()['taskid']
                if i.scheme =='http':
                    path = i.url.replace("http://"+i.host,"")
                else :
                    path = i.url.replace("https://"+i.host,"")
                packet = i.method+'  '+path+'  '+i.http_version+'\n'+i.request_headers+'\n\n'+i.request_content
                Sqlmap.objects.create(taskid=taskid,packet=packet)
                fp = open('taskid/'+taskid,'w+')
                fp.writelines(str(packet)+'\n')
                fp.close()
                
    def del_taskid(self):
        url = self.server + '/task/' + self.taskid + '/delete'
        
    def set_options(self):
        if self.options is None:
            return False
        else:
            url = self.server +"/option/"+self.taskid+"/set"
            data=json.dumps(self.options)
            responseData=requests.post(url,data=data,headers=self.header).json()['success']
            if responseData == True:
                return True
            else:
                return  False

    def list_options(self):
        url = self.server + '/option/' +self.taskid + '/list'
        
    def get_options(self):
        url = self.server  + '/option/' + self.taskid + '/get'
        
    
        
    def start_scan(self):
        for taskid in Sqlmap.objects.all().values('taskid'):
            taskid = taskid['taskid']
            payload = {'requestFile':os.path.join(BASE_DIR, 'taskid')+'/'+taskid}
            url = self.server + "/scan/" + taskid + "/start"
            t = json.loads(requests.post(url, data=json.dumps(payload), headers=self.headers).text)
        
        
    def stop_scan(self):
        url=self.server + "/scan/" + self.taskid +"/stop"
        
    def status_scan(self):
        url = self.server+'/scan/'+self.taskid+ '/status'
        
    def kill_scan(self):
        url = self.server + '/scan/'+self.taskid +'/kill'
        
    def data_scan(self):
        url = self.server + '/scan/' +self.taskid + '/data'
        self.data = requests.get(url).json()['data']
        if len(self.data)>0:
            return 'inject'
        else:
            return 'faild'
        
    

    def sqli_detail(self):
        url = self.server + '/scan/' +self.taskid + '/data'
        self.data = requests.get(url).json()['data']
        data1 = self.data[0]
        for i in data1:
            if isinstance(data1[i],dict):
                url = data1[i]['url']
                query = data1[i]['query']
                post_data = data1[i]['data']
                Sqlmap.objects.filter(taskid=self.taskid).update(url=url,query=query,post_data=post_data)
                
                
        data2 = self.data[1]
        for i in data2:
            if isinstance(data2[i],list):
                for i in data2[i]:
                    Sqlmap.objects.filter(taskid=self.taskid).update(dbms=i['dbms'],
                                                                     suffix=i['suffix'],
                                                                     clause=",".join(str(v) for v in i['clause']),
                                                                     notes = ",".join(str(v) for v in i['notes']),
                                                                     ptype = i['ptype'],
                                                                     dbms_version = ",".join(str(v) for v in i['dbms_version']),
                                                                     prefix = i['prefix'],
                                                                     place = i['place'],
                                                                     os = i['os'],
                                                                     parameter = i['parameter']
                                                                     )
                    if isinstance(i['data'], dict):
                        Sqlmap.objects.filter(taskid=self.taskid).update(detail=i['data']) 
            
                    
            
            

                
                    


            
        
        
    def run(self):
        pass
        
        
        
        