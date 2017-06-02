from __future__ import unicode_literals

from django.db import models

# Create your models here.
class scan(models.Model):
    host = models.CharField(max_length=20)
    hostname = models.CharField(max_length=100,blank=True)
    hostname_type = models.CharField(max_length=20)
    port = models.CharField(max_length=20)
    protocol = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10)
    product = models.CharField(max_length=40)
    extrainfo = models.CharField(max_length=40)
    reason = models.CharField(max_length=40)
    version = models.CharField(max_length=40)
    conf = models.CharField(max_length=40)
    cpe = models.CharField(max_length=40)
    time = models.DateField()

class UserInfo(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    mail = models.EmailField(max_length=50)
    def __unicode__(self):
        return self.username

class Sqlmap(models.Model):
    taskid = models.CharField(max_length=50)
    packet = models.TextField()
    url = models.TextField(default='')
    query = models.TextField(default='')
    post_data = models.TextField(default='',null=True)
    dbms = models.TextField(default='')
    suffix = models.TextField(default='')
    options = models.TextField(default='')
    clause = models.CharField(max_length=20,default='')
    notes = models.TextField(default='')
    ptype = models.CharField(max_length=20,default='')
    dbms_version = models.CharField(max_length=20,default='')
    prefix =models.TextField(default='')
    place = models.TextField(default='')
    os = models.TextField(default='',null=True)
    parameter =models.CharField(max_length=20,default='')
    detail = models.TextField(default='')


class Result(models.Model):
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
    http_version = models.CharField(max_length=20,default='')
'''
    def __unicode__(self):
        return self.method+'  '+self.url+' '+self.http_version+'\n'+self.request_headers+'\n\n'+self.request_content
'''
