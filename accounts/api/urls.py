from django.urls import path,include
from rest_framework_jwt.views import obtain_jwt_token,refresh_jwt_token

from . import views
urlpatterns = [
    path('',views.AuthAPIView.as_view(),name='login'),
    path('register/',views.RegisterAPIView.as_view(),name='register'),

    path('jwt/',obtain_jwt_token),#jwt auth
    path('jwt/refresh/',refresh_jwt_token),#jwt auth

    
]
