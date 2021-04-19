 
from django.urls import path
from updates.api.views import UpdateModelListAPIView,UpdateModelDetailAPIView

urlpatterns = [
    path('',UpdateModelListAPIView.as_view()),
    path('<int:id>/',UpdateModelDetailAPIView.as_view()),
]
