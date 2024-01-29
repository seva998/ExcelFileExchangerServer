from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('home_notstevedor/', views.home, name='home_notstevedor'),
    path('table1_data/', views.table1_data, name='table1_data'),
    path('success_table1/', views.success_table1, name='success_table1'),
    path('dataset/', views.dataset, name = 'dataset'),
    path('datepick_admin/', views.datepick_admin, name = 'datepick_admin'),
    path('table1_upload/', views.table1_upload, name = 'table1_upload'),
    path('table2_data/', views.table2_data, name='table2_data'),
    path('table2_upload/', views.table2_upload, name='table2_upload'),
    path('success_table2/', views.success_table2, name='success_table2'),
    re_path('download/', views.download, name='download'),
]