from django.shortcuts import render
from django.http import JsonResponse ,HttpResponse
from .models import Update
import json

from django.views.generic import View
from config.mixins import JsonResponseMixin
from django.core.serializers import serialize

# def detail_view(request):
#     # return  render() # return JSON data --> JS object

#obj = Update.objects.get(id=1)

def json_example_view(request):
    data ={
        "count":100,
        "content":"some new content"
    }
  
    json_data = json.dumps(data)
    # return JsonResponse(data)
    return HttpResponse(json_data,content_type="application/json")


class JsonCBV(View):
    def get(self,request,*args,**kwargs):

        data ={
            "count":1000,
            'content':"some new content"
        }
        json_data = json.dumps(data)
        return HttpResponse(json_data,content_type='application/json')

 

class JsonCBV2(JsonResponseMixin,View):
    def get(self,request,*args,**kwargs):
        data ={
            "count":1000,
            'content':"some new content"
        }
        return self.render_to_json_response(data)


class SerializeDetailView(View):
    def get(self,request,*args,**kwargs):
        obj = Update.objects.get(id=1)
        # data = serialize('json',[obj,],fields=('user','content'))
        # json_data=data
        json_data = obj.serialize()
        # data = {
        #     'user':obj.user.username,
        #     'content':obj.content
        # }
        #json_data = json.dumps(data)

        return HttpResponse(json_data,content_type="application/json")

class SerializeListView(View):
    def get(self,request,*args,**kwargs):
        # qs = Update.objects.all()
        # data = serialize("json",qs)#,fields=('user','content'))
        # print(data)
        # json_data =data

        json_data = Update.objects.all().serialize()
        # data = {
        #     'user':obj.user.username,
        #     'content':obj.content
        # }
        # json_data = json.dumps(data)

        return HttpResponse(json_data,content_type="application/json")
        