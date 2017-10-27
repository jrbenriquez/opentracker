"""prodtracker URL Configuration

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
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from tracker import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^team/(?P<team_id>[0-9]+)/$', views.team, name='team'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
    url(r'^user/new/$', views.NewUserView.as_view(), name='new_user'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event, name='event'),
    url(r'^event/new/$', views.new, name='new'),
    url(r'^event/new/(?P<parent_page>[A-z]+)/$', views.new_submit, name='new_submit'),
]
