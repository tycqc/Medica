from django.urls import path
from goods import views
from django.conf.urls import url

app_name = "goods"
urlpatterns = [
    path('index/', views.index.as_view(), name='index'),


]