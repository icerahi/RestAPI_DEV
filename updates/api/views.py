from updates.models import Update as UpdateModel
from django.views.generic import View
from django.http import HttpResponse
from config.mixins import  HttpResponseMixin,CSRFExemptMixin
import json 
from .forms import UpdateModelForm
from .utils import is_valid

class UpdateModelDetailAPIView(HttpResponseMixin,CSRFExemptMixin,View):
    """
    Retrive,Update,Delete ---->Object
    """
    is_json = True

    def get_object(self,id=None):
        # try:
        #     obj = UpdateModel.objects.get(id=id)
        # except UpdateModel.DoesNotExist:
        #     obj = None 
        """ Below handles a Does not exist exeption too"""

        qs = UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self,request,id,*args,**kwargs):
        obj = self.get_object(id=id)
        if obj is None :
            error_data = json.dumps({'message':'Update not found'})
            return self.render_to_response(error_data,status=404)
        
        #obj = UpdateModel.objects.get(id=id)
        json_data = obj.serialize()
        return self.render_to_response(json_data)
   
    def post(self,request,*args, **kwargs):
        json_data =json.dumps({'message':'Not allowed,please use the /api/update/ endpoint!'})
        return self.render_to_response(json_data,status=403)

    
    def put(self,request,id,*args, **kwargs):
        valid_json = is_valid(request.body)
        if not valid_json:
            error_data = json.dumps({"message":"Invalid data sent,please send using json"})
            return self.render_to_response(error_data,status=400)
        obj = self.get_object(id=id)
        if obj is None :
            error_data = json.dumps({'message':'Update not found'})
            return self.render_to_response(error_data,status=404)
        # new_data ={}
        data = json.loads(obj.serialize())
        passed_data = json.loads(request.body)
        for key,value in passed_data.items():
            data[key]=value 

        # save_data ={
        #     "user":obj.user,
        #     'content':obj.content 
        # }
    
        form = UpdateModelForm(passed_data,instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data,status=201)
       
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data,status=400)

        json_data =json.dumps({"message":"Something"})
        return self.render_to_response(json_data)

    def delete(self,request,id,*args, **kwargs):
        obj = self.get_object(id=id)
        if obj is None :
            error_data = json.dumps({'message':'Update not found'})
            return self.render_to_response(error_data,status=404)
       
        deleted_,item_deleted = obj.delete()
        print(deleted_)
        if deleted_ == 1:

            json_data =json.dumps({"message":"Successfully Deleted!"})
            return self.render_to_response(json_data,status=200)
        error_data = json.dumps({'message':'Could not delete item,Please try again later.'})
        return self.render_to_response(error_data,status=400)
       

#/api/update/
class UpdateModelListAPIView(HttpResponseMixin,CSRFExemptMixin,View):
    """
    ListView --->Retrieve -- DetailView
    CreateView
    Update
    Delete
    """
    is_json = True
    queryset = None 

    def get_queryset(self):
        qs = UpdateModel.objects.all()
        self.queryset = qs 
        return qs 
    
    
    def get_object(self,id=None):
        # try:
        #     obj = UpdateModel.objects.get(id=id)
        # except UpdateModel.DoesNotExist:
        #     obj = None 
        """ Below handles a Does not exist exeption too"""
        if id is None:
            return None 
        qs = self.get_queryset.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self,*args, **kwargs):
        data = json.loads(request.body)
        passed_id = data.get('id',None)
        if passed_id is not None:
            obj = self.get_object(id=passed_id)
            if obj is None:
                error_data = json.dumps({"message":"Object not found"})
                return self.render_to_response(error_data,status=400)
            json_data =obj.serialize()
            return self.render_to_response(json_data)
        else:
            qs = self.get_queryset()
            json_data = qs.serialize()
            return self.render_to_response(json_data)
   
    def post(self,request,*args, **kwargs):
        valid_json = is_valid(request.body)
        if not valid_json:
            error_data = json.dumps({"message":"Invalid data sent,please send using json"})
            return self.render_to_response(error_data,status=400)
        data = json.loads(request.body)
        form = UpdateModelForm(data)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data,status=201)
       
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data,status=400)

        data = json.dumps({'message':'Not Allowed'})
        return self.render_to_response(data,status=400)


    def put(self,request,*args, **kwargs):
        valid_json = is_valid(request.body)
        if not valid_json:
            error_data = json.dumps({"message":"Invalid data sent,please send using json"})
            return self.render_to_response(error_data,status=400)
       
        passed_data = json.loads(request.body)
        passed_id = passed_data.get('id',None)
        if not passed_id:
            error_data = json.dumps({"id":"This is a required field to update!!"})
            return self.render_to_response(error_data,status=400)
        
        obj = self.get_object(id=passed_id)
        if obj is None :
            error_data = json.dumps({'message':'Object not found'})
            return self.render_to_response(error_data,status=404)
        # new_data ={}
        data = json.loads(obj.serialize())
        for key,value in passed_data.items():
            data[key]=value 
        # save_data ={
        #     "user":obj.user,
        #     'content':obj.content 
        # }
        form = UpdateModelForm(passed_data,instance=obj)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data,status=201)
       
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data,status=400)

        json_data =json.dumps({"message":"Something"})
        return self.render_to_response(json_data)

    def delete(self,request,*args, **kwargs):
        valid_json = is_valid(request.body)
        if not valid_json:
            error_data = json.dumps({"message":"Invalid data sent,please send using json"})
            return self.render_to_response(error_data,status=400)
        passed_data = json.loads(request.body)
        passed_id = passed_data.get('id',None)
        if not passed_id:
            error_data = json.dumps({"id":"This is a required field to update!!"})
            return self.render_to_response(error_data,status=400)
        
        obj = self.get_object(id=passed_id)
        if obj is None :
            error_data = json.dumps({'message':'Object not found'})
            return self.render_to_response(error_data,status=404)
        deleted_,item_deleted = obj.delete()
        print(deleted_)
        if deleted_ == 1:
            json_data =json.dumps({"message":"Successfully Deleted!"})
            return self.render_to_response(json_data,status=200)
        error_data = json.dumps({'message':'Could not delete item,Please try again later.'})
        return self.render_to_response(error_data,status=400)
       