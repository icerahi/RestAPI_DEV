from django.urls import path,include
from .views import UserDetailApiView,UserStatusApiView
from . import views
urlpatterns = [
    path('<username>/',UserDetailApiView.as_view(),name='user_detail'),
    path('<username>/status/',UserStatusApiView.as_view(),name='user_status'),

]
