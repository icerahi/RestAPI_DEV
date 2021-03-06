from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from status.api.serializer import StatusSerializer
from status.models import Status 

## Serialize a single object ##
obj = Status.objects.first()
serializer = StatusSerializer(obj)
serializer.data 
json_data = JSONRenderer().render(serializer.data)
print(json_data)

stream =BytesIO(json_data)
data = JSONParser().parse(stream)
print(data) 


### Serialize a queryset
qs = Status.objects.all()
serializer2=StatusSerializer(qs,many=True)
serializer2.data 
json_data2=JSONRenderer().render(serializer2.data)
print(json_data2)

stream2 = BytesIO(json_data2)
data2 =JSONParser().parse(steam2) 
print(data2)


# create obj
data = {'user':1}
serializer = StatusSerializer(data=data)
serializer.is_valid()
serializer.save()
# if serializer.is_valid():
#     serializer.save()

# update obj

obj = Status.objects.first()
data = {'content':'update contented','user':1}
update_serializer = StatusSerializer(obj,data=data)
update_serializer.is_valid()
update_serializer.save()

# Delete obj
 
data = {'user':1,'content':'please delete me!'}
create_obj_serializer = StatusSerializer(data=data)
create_obj_serializer.is_valid()
create_obj = create_obj_serializer.save() # instance of obj
print(create_obj)

obj = Status.objects.last()
get_data_serializer = StatusSerializer(obj)
print(obj.delete())
print(get_data_serializer.data)



# test custom serializer
from rest_framework import serializers
class CustomSerializer(serializers.Serializer):
    content = serializers.CharField()
    email   = serializers.EmailField()


data = {'email':"rahi@gmail.com",'content':'please delete me!'}
create_obj_serializer = CustomSerializer(data=data)
if create_obj_serializer.is_valid():
    valid_data = create_obj_serializer.data
    print(valid_data)
 
