from django.urls import path
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from user import views

app_name = "store"
urlpatterns = [
    url(r'^login/', views.LoginView.as_view()),
    url(r'^message/', views.MessageView.as_view()),


]