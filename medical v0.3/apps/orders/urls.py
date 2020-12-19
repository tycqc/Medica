from django.urls import path
from orders import views
from django.conf.urls import url

app_name = "orders"
urlpatterns = [
    path('order_details/', views.order_details, name='order_details'),
    path('order_list/', views.order_list, name='order_list'),
    path('find_order_data/', views.find_order_data, name='find_order_data'),
    path('del_order/', views.del_order, name='del_order'),
    path('staff_order_add/', views.staff_order_add, name='staff_order_add'),
    path('get_tag/', views.get_tag, name='get_tag'),
    path('finance/', views.finance, name='finance'),
    # path('finance_days_datas/', views.finance_days_datas, name='finance_days_datas'),
    path('order_add/', views.order_add.as_view(), name='order_add'),
    path('order_li/', views.order_li.as_view(), name='order_li'),
    path('order_det/', views.order_det.as_view(), name='order_det'),
]