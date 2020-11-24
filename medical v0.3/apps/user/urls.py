from django.urls import path
from django.conf.urls import url
from apps.user import views

app_name = "store"
urlpatterns = [
    url(r'^login/', views.LoginView.as_view()),
    url(r'^message/', views.MessageView.as_view()),
    url(r'^edit/', views.EditView.as_view()),


]