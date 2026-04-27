from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path('', views.media_list, name='home'),
    path('media/<int:pk>/', views.media_detail, name='detail'),
    path('upload/', views.media_upload, name='upload'),
]
