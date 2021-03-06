"""geekpy_6 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static

from post import views as post_views
from user import views as user_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_views.post_list),
    url(r'^(?P<blog_pk>\d+)/$', user_views.user_info),
    url(r'^index/$', post_views.post_list),
    url(r'^post/read/(?P<post_pk>\d+)', post_views.post_read),
    url(r'^post/add', post_views.post_add),
    url(r'^post/list', post_views.post_list),
    url(r'^post/edit/(?P<post_pk>\d+)', post_views.post_edit),
    url(r'^user/login', user_views.login),
    url(r'^user/logout', user_views.logout),
    url(r'^user/register', user_views.register),
    url(r'^user/info', user_views.user_info),
    url(r'^user/fill', user_views.fill_info),
    url(r'^user/edit/', user_views.edit_info),
    url(r'^blog/(?P<blog_pk>\d+)', user_views.user_info),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
