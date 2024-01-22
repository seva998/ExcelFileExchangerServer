from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('confirm/', views.confirm, name='confirm'),
    path('success/', views.success, name='success'),
    path('dataset/', views.dataset, name = 'dataset'),
    path('datepick/', views.datepick, name = 'datepick'),
    re_path('download/', views.download, name='download'),
]