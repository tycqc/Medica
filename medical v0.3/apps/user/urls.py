from django.urls import path
from django.conf.urls import url
from user import views

app_name = "user"
urlpatterns = [
    url(r'^login/', views.LoginView.as_view()),
    url(r'^message/', views.MessageView.as_view()),


]