"""medical URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include,re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from store.views import login


urlpatterns = [
    path('admin/', admin.site.urls),

    re_path('staff/', include(('staff.urls', 'staff'), namespace='staff')),
    re_path('medicine/', include(('medicine.urls', 'medicine'), namespace='medicine')),
    re_path('store/', include(('store.urls', 'store'), namespace='store')),
    re_path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    re_path('salesDATA/', include(('salesDATA.urls', 'salesDATA'), namespace='salesDATA')),
    re_path('user/', include(('user.urls', 'user'), namespace='user')),
    re_path('goods/', include(('goods.urls', 'goods'), namespace='goods')),
    path('search/', include('search.urls')),
    path('', login),
]
