from django.urls import re_path
from toys import views

urlpatterns = [
    re_path('^toys/$', views.toy_list),
    re_path(r'^toys/(?P<pk>[0-9]+)/$', views.toy_detail),
]