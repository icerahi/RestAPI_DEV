from django.http import JsonResponse,HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class HttpResponseMixin(object):
    is_json = False 
    def render_to_response(self,data,status=200):
        content_type = 'text/html'
        if self.is_json:
            content_type='application/json'
        return HttpResponse(data,content_type=content_type,status=status)


class JsonResponseMixin(object):
    def render_to_json_response(self,context,**response_kwargs):
        return JsonResponse(self.get_data(context),**response_kwargs)


    def get_data(self,context):
        return context 


class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self,*args,**kwargs):
        return super().dispatch(*args,**kwargs)

