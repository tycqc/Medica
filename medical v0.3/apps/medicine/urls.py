from django.urls import path
from medicine import views
from django.conf.urls import url

app_name = "medicine"
urlpatterns = [
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('find_medicine/', views.find_medicine, name='find_medicine'),
    path('edit_medicine/', views.edit_medicine, name='edit_medicine'),
    path('del_medicine/', views.del_medicine, name='del_medicine'),
    path('medicine_detail/', views.medicine_detail, name='medicine_detail'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart_list/', views.cart_list, name='cart_list'),
    path('cart_list_data/', views.cart_list_data, name='cart_list_data'),
    path('del_cart_list/', views.del_cart_list, name='del_cart_list'),
    # path('shiyan/', views.shiyan, name='shiyan'),
    path('find_medicine_data/', views.find_medicine_data, name='find_medicine_data'),

]