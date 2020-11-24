from django.urls import path
from apps.store import views
from django.conf.urls import url

app_name = "store"
urlpatterns = [
    url(r'^register$', views.register, name='register'), # 注册
    url(r'^login$', views.login, name='login'), # 登录
    url(r'^logout$', views.logout, name='logout'), # 退出账号
    url(r'^homepage$', views.store_homepage, name='homepage'),  # 用户中心-信息主页
    url(r'^homepage_update$', views.store_homepage_update, name='homepage_update'),  # 用户中心-修改信息
    url(r'^cancellation$', views.store_cancellation, name='cancellation'),  # 用户中心-注销账户

]