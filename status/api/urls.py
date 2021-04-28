from django.urls import path
from . import views

urlpatterns = [
  path('',views.StatusListSearchAPIView.as_view(),name='home'),
#   path('create/',views.StatusCreateAPIView.as_view()),
  path('<int:pk>/',views.StatusDetailAPIView.as_view(),name='status-detail'),
#   path('<int:pk>/update/',views.StatusUpdateAPIView.as_view()),
#   path('<int:pk>/delete/',views.StatusDeleteAPIView.as_view()),
]

""" 
#start with
/api/status/ -> List
/api/status/create -> Create
/api/status/<id>/  -> Detail
/api/status/<id>/update -> Update
/api/status/<id>/delete  -> Delete

# End with
/api/status -> List -> CRUD
/api/status/<id>/ - Detail -> CRUD

#Final
/api/status/ -> CRUD & LS
"""