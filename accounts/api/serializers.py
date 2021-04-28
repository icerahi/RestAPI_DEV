from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime
from rest_framework_jwt.settings import api_settings
from rest_framework.reverse import reverse as drf_reverse

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER
expire_delta = api_settings.JWT_REFRESH_EXPIRATION_DELTA

User = get_user_model()

 

#nested serializer
class UserPublicSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User 
        fields = [
            'uri',
            'id',
            'username',
            
            ]

    def get_uri(self,obj):
        request = self.context.get('request',None)
        return drf_reverse('user_detail',kwargs={'username':obj.username},request=request)

 


class UserRegisterSerializer(serializers.ModelSerializer):
    password    = serializers.CharField(write_only=True,style={'input_type':'password'})
    password2    = serializers.CharField(write_only=True,style={'input_type':'password'})
    email        = serializers.EmailField(required=True)
   
    token       = serializers.SerializerMethodField(read_only=True)
    expires_token     = serializers.SerializerMethodField(read_only=True)
    #token_response = serializers.SerializerMethodField(read_only=True)
    message       = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model   = User 
        fields  = [
            'username',
            'email',
            'password',
            'password2',

            'token',
            'expires_token',
            #'token_response',
            'message',
        ]
        extra_kwargs = {'password':{'write_only':True}}

    def get_message(self,obj):
        return "Thanks for Registering! Please Complete Your Profile!!"

    # #token response
    # def get_token_response(self,obj):
    #     user = obj 
    #     payload = jwt_payload_handler(user)
    #     token   = jwt_encode_handler(payload)
    #     context = self.context 
    #     request = context['request']    #getting context from view
    #     print(request.user.is_authenticated)
    #     response = jwt_response_payload_handler(token=token,user=user,request=context['request'])
    #     return response 
  
    #get token expire time
    def get_expires_token(self,obj):
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)
   
    def get_token(self,obj): #get instance of the model
        user = obj 
        payload = jwt_payload_handler(user)
        token   = jwt_encode_handler(payload)
        return token 

    #validate email
    def validate_email(self,value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("User with this Email already registered!")
        return value
        
    #validate username
    def validate_username(self,value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username already exists!")
        return value 

    def validate(self,data):
        pw = data.get('password')
        pw2= data.pop('password2')
        if pw != pw2:
            raise serializers.ValidationError('Password must match')

        return data


    def create(self,validated_data):
        user_obj = User(username=validated_data.get('username'),
        email=validated_data.get('email'))
        
        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = False # for email verification
        user_obj.save()
        return user_obj
