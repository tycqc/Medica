from django.urls import path
from apps.orders import views
from django.conf.urls import url

app_name = "orders"
urlpatterns = [
    path('order_details/', views.order_details, name='order_details'),
    path('order_list/', views.order_list, name='order_list'),
    path('del_order/', views.del_order, name='del_order'),
    path('staff_order_add/', views.staff_order_add, name='staff_order_add'),
    path('get_tag/', views.get_tag, name='get_tag'),
    path('finance/', views.finance, name='finance'),
]