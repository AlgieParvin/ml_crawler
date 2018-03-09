from django.urls import path, re_path

from core import views


REDDIT = 'reddit'
ML_MASTERY = 'Machine Learning Mastery'
ML_WEEKLY = 'Machine Learning Weekly'
MIT_NEWS = 'Mit News'


urlpatterns = [
    path('', views.reddit),
    path('reddit/', views.reddit, name=REDDIT),
    path('ml_mastery/', views.machine_learning_mastery, name=ML_MASTERY),
    path('ml_weekly/', views.machine_learning_weekly, name=ML_WEEKLY),
    path('mit/', views.mit, name=MIT_NEWS),

    re_path(r'^ml_mastery/(?P<period>\w{0,50})/$', views.machine_learning_mastery, name=ML_MASTERY),
    re_path(r'^reddit/(?P<period>\w{0,50})/$', views.reddit, name=REDDIT),
    re_path(r'^ml_weekly/(?P<period>\w{0,50})/$', views.machine_learning_weekly, name=ML_WEEKLY),
    re_path(r'^mit/(?P<period>\w{0,50})/$', views.mit, name=MIT_NEWS),

    re_path(r'^ml_mastery/(?P<period>\w{0,50})/(?P<page>\d+)/$', views.machine_learning_mastery, name=ML_MASTERY),
    re_path(r'^reddit/(?P<period>\w{0,50})/(?P<page>\d+)/$', views.reddit, name=REDDIT),
    re_path(r'^ml_weekly/(?P<period>\w{0,50})/(?P<page>\d+)/$', views.machine_learning_weekly, name=ML_WEEKLY),
    re_path(r'^mit/(?P<period>\w{0,50})/(?P<page>\d+)/$', views.mit, name=MIT_NEWS),
]
