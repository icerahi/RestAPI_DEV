from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as drf_reverse
from status.api.serializers import StatusInlineUserSerializer

User = get_user_model()

class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)
    #status_uri = serializers.SerializerMethodField(read_only=True)
    #recent_status = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    
    # statuses   = serializers.HyperlinkedRelatedField(
    #     source='status_set',#Status.objects.filter(user=user)
    #     many=True, read_only=True,
    #     lookup_field='pk',
    #     view_name="status-detail",
    # ) #all status as link will here

    # statuses    = StatusInlineUserSerializer(source='status_set',many=True,read_only=True)

    class Meta:
        model = User 
        fields = [
            # 'statuses',
            'uri',
            'id',
            'username',
            #'status_uri',
            #'recent_status',
            'status' #model name
            ]

    def get_uri(self,obj):
        request = self.context.get('request')
        return drf_reverse('user_detail',kwargs={'username':obj.username},request=request)
        # return drf_reverse('<namespace:<view_name>',kwargs={'username':obj.user.username})

    # def get_status_uri(self,obj):
    #     return self.get_uri(obj)+'status/'
   
    def get_status(self,obj):
        request = self.context.get('request')
        limit = 5 

        if request:
            #endpoint: /?limit=<int>
            limit_query = request.GET.get('limit')
            try:
                limit = int(limit_query)
            except:
                pass

        qs = obj.status_set.all().order_by('-timestamp')#[:5] # Status.objects.filter(user=obj)
        data = {
            'uri':self.get_uri(obj)+'status/',
            'last':StatusInlineUserSerializer(qs.first(),context={'request':request}).data,
            'recent_'+str(limit): StatusInlineUserSerializer(qs[:limit],many=True,context={'request':request}).data,
        }
        return data

    # def get_recent_status(self,obj):
    #     qs = obj.status_set.all().order_by('-timestamp')[:2] # Status.objects.filter(user=obj)
        
    #     return StatusInlineUserSerializer(qs,many=True).data

