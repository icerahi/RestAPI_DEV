from rest_framework import permissions,generics,pagination
from django.contrib.auth import get_user_model
  
from .serializers import UserDetailSerializer
from accounts.api.permissions import anonPermissionOnly
from status.models import Status
from status.api.serializers import StatusInlineUserSerializer
from status.api.views import StatusListSearchAPIView
from rest_framework.response import Response
User = get_user_model()

class UserDetailApiView(generics.RetrieveAPIView):
  #  permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset    = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
    lookup_field    ='username' #id

    def get_serializer_context(self):
        return {'request':self.request}


 #for custom pagination
# class StatusAPIPagination(pagination.PageNumberPagination):
#     page_size = 2


# class UserStatusApiView(generics.ListAPIView):
#     serializer_class = StatusInlineUserSerializer
#     search_fields    = ('user__username','content',)
#     # pagination_class = StatusAPIPagination

#     def get_queryset(self,*args, **kwargs):
#         username = self.kwargs.get('username',None)
#         if username is None :
#             return Status.objects.none()
#         return Status.objects.filter(user__username=username)


class UserStatusApiView(StatusListSearchAPIView):
    serializer_class = StatusInlineUserSerializer
    def get_queryset(self,*args, **kwargs):
        username = self.kwargs.get('username',None)
        if username is None :
            return Status.objects.none()
        return Status.objects.filter(user__username=username)

    def post(self,request,*args, **kwargs):
        return Response({'detail':'Now allowed here'},status=400)
        
