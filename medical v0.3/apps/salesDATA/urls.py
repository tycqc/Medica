from django.urls import path
from orders import views
from django.conf.urls import url

app_name = "salesDATA"
urlpatterns = [
    path('finance/', views.finance, name='finance'),
    path('finance_days_datas/', views.finance_days_datas, name='finance_days_datas'),
]