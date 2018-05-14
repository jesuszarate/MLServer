from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^upload_picture', views.uploadPicture, name='uploadPicture'),
    url(r'^pp', views.upload_pic, name='pp'),
    url(r'^jj', views.jj, name='jj'),
    url(r'^rs', views.recSystem, name='rs'),
    url(r'^$', views.index, name='index'),
    
]
