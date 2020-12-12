from django.urls import path
from salesDATA import views
from django.conf.urls import url

app_name = "salesDATA"
urlpatterns = [
    # path('finance/', views.finance, name='finance'),
    path('finance_medicine/', views.finance_medicine, name='finance_medicine'),
    path('finance_staff/', views.finance_staff, name='finance_staff'),
    path('finance_month/', views.finance_month, name='finance_month'),
    path('finance_year/', views.finance_year, name='finance_year'),
    path('finance_medicine_datas/', views.finance_medicine_datas, name='finance_medicine_datas'),
    path('finance_staff_datas/', views.finance_staff_datas, name='finance_staff_datas'),
    path('finance_month_datas/', views.finance_month_datas, name='finance_month_datas'),
    path('finance_year_datas/', views.finance_year_datas, name='finance_year_datas'),
    path('Echarts/', views.Echarts, name='Echarts'),
]