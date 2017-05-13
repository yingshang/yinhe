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


class Result(models.Model):
    host = models.TextField()
    url = models.TextField()
    method = models.CharField(max_length=20)
    request_headers = models.TextField()
    scheme = models.TextField()
    path = models.TextField()
    port = models.CharField(max_length=20)
    status_code = models.CharField(max_length=20)
    response_headers = models.TextField()
    response_content = models.TextField()
    date =models.TimeField(auto_now=True)
    request_content = models.TextField()