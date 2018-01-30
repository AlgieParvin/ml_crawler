from django.urls import path, re_path

from core import views

urlpatterns = [
    path('reddit/', views.reddit),
    path('ml_mastery/', views.machine_learning_mastery),
    re_path(r'ml_mastery/(?P<period>\w{0,50})/', views.machine_learning_mastery, name='Machine Learning Mastery'),
    re_path(r'reddit/(?P<period>\w{0,50})/', views.reddit, name='reddit'),
]
