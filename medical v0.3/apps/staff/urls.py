from django.urls import path
from staff import views
from django.conf.urls import url

app_name = "staff"
urlpatterns = [
    path('register_staff/', views.register_staff, name='register_staff'),
    path('find_staff/', views.find_staff, name='find_staff'),
    path('edit_staff/', views.edit_staff, name='edit_staff'),
    path('del_staff/', views.del_staff, name='del_staff'),
    path('detail_staff/', views.detail_staff, name='detail_staff'),
]