from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^upload_picture', views.uploadPicture, name='uploadPicture'),
    url(r'^pp', views.upload_pic, name='pp'),
    url(r'^jj', views.jj, name='jj'),
    url(r'^rankade_scores', views.record_rankade_score, name='rankade_scores'),
    url(r'^send_rankade_scores', views.send_rankade_scores, name='send_rankade_scores'),
    url(r'^rs', views.recSystem, name='rs'),
    url(r'^get_ids', views.get_ids, name='get_ids'),
    url(r'^load_ids', views.load_ids, name='load_ids'),
    url(r'^$', views.index, name='index'),
    
]
