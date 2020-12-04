from django.urls import path
from goods import views
from django.conf.urls import url

app_name = "goods"
urlpatterns = [
    path('index/', views.index.as_view(), name='index'),
    path('detail/', views.detail.as_view(), name='detail'),
    path('search/', views.search.as_view(), name='search'),


]