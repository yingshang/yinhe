"""yinhe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#from django.contrib.auth import views as login_views
from scan import views as scan_views
from scan import sqlinjection
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^login/',login_views.login,{'templates':'login.html'},name='login'),
    url(r'^capture/',scan_views.capture),
    url(r'^start_scan/',scan_views.start_scan),
    url(r'^nm_scan/',scan_views.nm_scan),
    #url(r'^index/',scan_views.capture_data),
    #url(r'^detail_data/$',scan_views.detail_data),
    #url(r'^del_data/(?P<id>\d+)',scan_views.del_data),
    #url(r'^flush_data/',scan_views.flush_data),
    #url(r'^sqli/(?P<taskid>\w+)/$',scan_views.sqli),
    #url(r'^sqli_detail/(?P<taskid>\w+)/$',scan_views.sqli_detail),
]
