# ** ADD NEW PAGES IN THIS URLS.PY - leave the one in rbs_app alone!

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]