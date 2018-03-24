from django.db import models
import datetime
# Create your models here.

class inject_data(models.Model):
    taskid = models.CharField(max_length=50)
    packet = models.TextField(default='')
    url = models.TextField(default='')
    query = models.TextField(default='')
    post_data = models.TextField(default='', null=True)
    dbms = models.TextField(default='')
    suffix = models.TextField(default='')
    run_status = models.CharField(max_length=50,default='')
    status = models.CharField(max_length=10,default='0')
    options = models.TextField(default='')
    clause = models.CharField(max_length=20, default='')
    notes = models.TextField(default='')
    ptype = models.CharField(max_length=20, default='')
    dbms_version = models.CharField(max_length=20, default='')
    prefix = models.TextField(default='')
    place = models.TextField(default='')
    vul_info = models.CharField(max_length=100,default='')
    os = models.TextField(default='', null=True)
    parameter = models.CharField(max_length=20, default='')
    detail = models.TextField(default='')
    time = models.DateTimeField(default=datetime.datetime.now())


class filter_data(models.Model):
    data_packet = models.TextField()
    url = models.CharField(max_length=500)
    parm = models.TextField()
    status = models.CharField(max_length=10,default='0')
    taskid = models.CharField(max_length=100,default='')

class proxy_data(models.Model):
    host = models.TextField(default='')
    url = models.TextField(default='')
    method = models.CharField(max_length=20,default='')
    request_headers = models.TextField(default='')
    scheme = models.TextField(default='')
    path = models.TextField(default='')
    request_cookies = models.TextField(default='')
    port = models.CharField(max_length=20,default='')
    status_code = models.CharField(max_length=20,default='')
    response_headers = models.TextField(default='')
    response_content = models.TextField(default='')
    date =models.TimeField(auto_now=True)
    request_content = models.TextField()
    http_version = models.CharField(max_length=20)

class config(models.Model):
    name = models.CharField(max_length=100)
