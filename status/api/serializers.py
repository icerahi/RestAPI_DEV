from rest_framework import serializers
from status.models import Status as Status
from accounts.api.serializers import UserPublicSerializer
from rest_framework.reverse import reverse as drf_reverse
 


class StatusSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    user = UserPublicSerializer(read_only=True )
    # user = serializers.PrimaryKeyRelatedField(read_only=True)#default
    # user_id = serializers.PrimaryKeyRelatedField(source='user',read_only=True)#default
   
    # user_id = serializers.HyperlinkedRelatedField(
    #     source='user', #user foreignkey
    #     lookup_field='username',
    #     view_name='user_detail',
    #     read_only=True)

    # username = serializers.SlugRelatedField(source='user',read_only=True,slug_field='username')#'email')
    # user = serializers.SlugRelatedField(read_only=True,slug_field='username')#'email')

    class Meta:
        model = Status
        fields = (
           # 'username',
          #  'user_id',
            'uri',
            'id',
            'user',
            'content',
            'image',)
        read_only_fields = ['user'] #GET
    

    def get_uri(self,obj):
        request = self.context.get('request')
        return drf_reverse('status-detail',kwargs={'pk':obj.pk},request=request)

    #serializer validation
    def validate_content(self,value):
        if len(value) >400:
            raise serializers.ValidationError("This way too long")
        return value

    def validate(self,data):
        content = data.get('content', None)
        if content == "":
            content = None 

        image = data.get('image',None)
        if content is None and image is None :
            raise serializers.ValidationError('Content or image is required!')
        return data


class StatusInlineUserSerializer(StatusSerializer):
   # uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = (
            'uri',
            'id',
            'content',
            'image',)
        read_only_fields = ['user'] #GET
    
 
# class StatusInlineUserSerializer(serializers.ModelSerializer):
#     uri = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = Status
#         fields = (
#             'uri',
#             'id',
#             'content',
#             'image',)
#         read_only_fields = ['user'] #GET
    
    
#     def get_uri(self,obj):
#         request = self.context.get('request')
#         return drf_reverse('status-detail',kwargs={'pk':obj.pk},request=request)