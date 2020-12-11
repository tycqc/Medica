from django.urls import path
from salesDATA import views
from django.conf.urls import url

app_name = "salesDATA"
urlpatterns = [
    # path('finance/', views.finance, name='finance'),
    path('finance_medicine_datas/', views.finance_medicine_datas, name='finance_medicine_datas'),

]