from django.db import models
from django.conf import settings
from django.core.serializers import serialize
import json

class UpdateQuerySet(models.QuerySet):
    # def serialize(self):
    #     qs = self
    #     final_array = []
    #     for obj in qs:
    #         stuct = json.loads(obj.serialize())
    #         final_array.append(stuct)
    #     return json.dumps(final_array)

    def serialize(self):
        list_values = list(self.values('id','user','content','image'))
        return json.dumps(list_values)


class UpdateManager(models.Manager):
    def get_queryset(self):
        return UpdateQuerySet(self.model,using=self._db)

def upload_update_image(instance,filename):
    return "updates/{user}/{filename}".format(user=instance.user,filename=filename)



class Update(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to=upload_update_image,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = UpdateManager()
    def __str__(self):
        return self.content or ""

    def serialize(self):
        try:
            image = self.image.url 
        except:
            image =""
        data ={
            'id':self.id,
            'user':self.user.id,
            'content':self.content ,
            'image':image
        }
        # json_data = serialize('json',[self],fields=('user','content','image'))
        # stuct = json.loads(json_data)
        # data = json.dumps(stuct[0]['fields'])
        return json.dumps(data)
    