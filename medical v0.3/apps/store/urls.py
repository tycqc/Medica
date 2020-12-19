from django.urls import path
from store import views
from django.conf.urls import url

app_name = "store"
urlpatterns = [
    url(r'^register$', views.register, name='register'), # 注册
    path('login/', views.login, name='login'), # 登录
    url(r'^logout$', views.logout, name='logout'), # 退出账号
    url(r'^homepage$', views.store_homepage, name='homepage'),  # 用户中心-信息主页
    url(r'^homepage_update$', views.store_homepage_update, name='homepage_update'),  # 用户中心-修改信息
    url(r'^cancellation$', views.store_cancellation, name='cancellation'),  # 用户中心-注销账户
    url(r'^email_s$', views.email_s, name='email_s'),  # 用户中心-发送验证码
    url(r'^email_s2$', views.email_s2, name='email_s2'),  # 用户中心-发送验证码
    path('forget_password/', views.forget_password, name='forget_password'),  # 用户中心-忘记密码-邮箱验证
    path('reset_password/', views.reset_password, name='reset_password'),  # 用户中心-忘记密码-邮箱验证
    url(r'^forget_email$', views.forget_email, name='forget_email'),  # 用户中心-忘记密码-忘记邮箱
    url(r'^email_check$', views.email_check, name='email_check'),  # 用户中心-邮箱验证
    path('store_li/', views.store_li.as_view(), name='store_li'),
    path('store_det/', views.store_det.as_view(), name='store_det'),


    # url(r'^shiyan$', views.shiyan, name='shiyan'),
    # url(r'^shiyan_index$', views.shiyan_index, name='shiyan_index'),
]