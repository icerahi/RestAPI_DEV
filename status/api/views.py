from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import StatusSerializer
from status.models import Status
from rest_framework import generics,mixins,permissions
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication
from accounts.api.permissions import IsOwnerOrReadOnly

# detail,update,delete in single view
class StatusDetailAPIView(mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.RetrieveAPIView):

    permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    # authentication_classes = []
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def put(self,request,*args, **kwargs):
        return self.update(request,*args, **kwargs) 

    def delete(self,*args, **kwargs):
        return self.destroy(self.request,*args, **kwargs)


class StatusListSearchAPIView(mixins.CreateModelMixin,generics.ListAPIView):

    permission_classes=[permissions.IsAuthenticatedOrReadOnly,]
    # authentication_classes=[SessionAuthentication,]
    serializer_class = StatusSerializer
    search_fields   = ('user__username','content','user__email')
    ordering_fields = ('user__username','timestamp',)
    queryset = Status.objects.all()

    # def get_queryset(self):
    #    # print(self.request.user)
    #     qs = Status.objects.all()
    #     query = self.request.GET.get('search') 
    #     if query is not None:
    #         qs = qs.filter(content__icontains=query)#.filter(user__username='')
    #     return qs 
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



















# #all in one endpoint
# class StatusListSearchAPIView(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.CreateModelMixin,
#     generics.ListAPIView):

#     permission_classes=[]
#     authentication_classes = []
#     #queryset = Status.objects.all()
#     serializer_class = StatusSerializer

#     def get_queryset(self):
#         qs =  Status.objects.all()
#         #search functionality /?q=
#         query = self.request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(content__icontains=query)
#             return qs 
#         return qs
    
#     def get_object(self):
#         request = self.request
#         #get single object /?id=id
#         passed_id = request.GET.get('id',None)
#         queryset = self.get_queryset()
#         obj = None 
#         if passed_id is not None:
#             obj = get_object_or_404(queryset,id=passed_id)
#             self.check_object_permissions(request,obj)
#         return obj
#     #overriding list queryset.
#     def get(self,request,*args,**kwargs):
#         passed_id = request.GET.get('id',None)
#         if passed_id is not None:
#             return self.retrieve(request,*args,**kwargs)
#         return super().get(request,*args,**kwargs)

#     def post(self,request,*args, **kwargs):
#         return self.create(request,*args, **kwargs)
    
#     def put(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)
    
#     def patch(self,request,*args,**kwargs):
#         return self.update(request,*args,**kwargs)

#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request,*args,**kwargs)

#     # def perform_create(self, serializer): #default user
#     #     serializer.save(user=self.request.user)
















# # CreateModelMixin ---handle Post Method
# # UpdateModelMixin ---handle Put Method
# # DestroyModelMixin -- handle Delete Method

# #only get api view
# class StatusAPIView(APIView):
#     permission_classes=[]
#     authentication_classes = []

#     def get(self,request,format=None):
#         qs = Status.objects.all()
#         serializer = StatusSerializer(qs,many=True)
#         return Response(serializer.data)

#     def post(self,request,format=None):
#         pass
 
# # list search ,create endpoint
# class StatusListSearchAPIView(mixins.CreateModelMixin,generics.ListAPIView):
#     permission_classes=[]
#     authentication_classes = []
#     #queryset = Status.objects.all()
#     serializer_class = StatusSerializer

#     def get_queryset(self):
#         qs =  Status.objects.all()
#         #search functionality /?q=
#         query = self.request.GET.get('q')
#         if query is not None:
#             qs = qs.filter(content__icontains=query)
#             return qs 
#         return qs

#     def post(self,request,*args, **kwargs):
#         return self.create(request,*args, **kwargs)

#     # def perform_create(self, serializer): #default user
#     #     serializer.save(user=self.request.user)

# # single create endpoint
# # class StatusCreateAPIView(generics.CreateAPIView):
# #     permission_classes=[]
# #     authentication_classes = []
# #     queryset = Status.objects.all()
# #     serializer_class = StatusSerializer

#     # def perform_create(self, serializer): #default user
#     #     serializer.save(user=self.request.user)

# # detail,update,delete in single view
# class StatusDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes=[]
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer


# #detail,update,delete endpoint with different mixins
# class StatusDetailAPIView(mixins.DestroyModelMixin,mixins.UpdateModelMixin,generics.RetrieveAPIView):
#     permission_classes=[]
#     authentication_classes = []
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     #lookup_field = 'id'

#     # def get_object(self,*args, **kwargs):
#     #     kwargs = self.kwargs
#     #     kw_id  = kwargs['id']
#     #     return Status.objects.get(id=kw_id)

#     def put(self,request,*args, **kwargs):
#         return self.update(request,*args, **kwargs)

#     def delete(self,request,*args, **kwargs):
#         return self.destroy(request,*args,**kwargs)
    

# # single update endpoint
# # class StatusUpdateAPIView(generics.UpdateAPIView):
# #     permission_classes=[]
# #     authentication_classes = []
# #     queryset = Status.objects.all()
# #     serializer_class = StatusSerializer
 
# # single delete endpoint
# # class StatusDeleteAPIView(generics.DestroyAPIView):
# #     permission_classes=[]
# #     authentication_classes = []
# #     queryset = Status.objects.all()
# #     serializer_class = StatusSerializer