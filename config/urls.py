"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
from updates import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/updates/',include('updates.api.urls')),
    path('json/cbv1/',views.JsonCBV.as_view()),
    path('json/cbv2/',views.JsonCBV2.as_view()),
    path('json/example/',views.json_example_view),
    path('json/serialize/list/',views.SerializeListView.as_view()),
    path('json/serialize/detail/',views.SerializeDetailView.as_view())
]
