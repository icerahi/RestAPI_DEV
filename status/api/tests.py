from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as drf_reverse
from django.contrib.auth import get_user_model
from status.models import Status

from rest_framework import status 
 
import os 
import shutil
import tempfile
from PIL import Image 
from django.conf import settings
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler  = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

class StatusAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='rahi',email='rahi@gmail.com')
        user.set_password('rahirahi')
        user.save() 

        status_obj = Status.objects.create(user=user,content='hello there!')

 

    def test_statuses(self):
        self.assertEqual(Status.objects.count(), 1)
   
    def test_user_token(self):
        auth_url = drf_reverse('login')
        auth_data = {'username':'rahi','password':'rahirahi'}
        auth_response=self.client.post(auth_url,auth_data,format='json')
        token = auth_response.data.get('token',0)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
    
    def create_item(self):
        self.test_user_token()
        url = drf_reverse('home')
        data={'content':'some cool test content'}
        response=self.client.post(url,data,format='json') 
        self.assertEqual(response.status_code,status.HTTP_201_CREATED )
        self.assertEqual(Status.objects.count(), 2)
        return response.data

    def test_empty_create_item(self):
        self.test_user_token()
        url = drf_reverse('home')
        data={
            #'content':'some cool test content'
            }
        response=self.client.post(url,data,format='json') 
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST )
        return response.data


    def test_status_create_with_image_and_content(self):
        self.test_user_token()
        url = drf_reverse('home')
        #(w,h)=(800,1280)
        #color = (255,255,255)
        image_item = Image.new('RGB',(800,1280),(0,124,174))
        temp_file=tempfile.NamedTemporaryFile(suffix='.jpg')
        image_item.save(temp_file,format='JPEG')

        with open(temp_file.name,'rb') as file_obj:

            data={
                'content':'some cool test content',
                'image':file_obj,
                }
            response=self.client.post(url,data,format='multipart') 
            print(response.data)
            img_data = response.data.get('image')
            self.assertNotEqual(img_data, None)
            self.assertEqual(response.status_code,status.HTTP_201_CREATED )
            self.assertEqual(Status.objects.count(), 2)
             
        #remove temp img
        temp_img_dir = os.path.join(settings.MEDIA_ROOT,'status','rahi')
        print(temp_img_dir)
        if os.path.exists(temp_img_dir):
            print('yes exists')
            shutil.rmtree(temp_img_dir)

    def test_status_create_with_image_no_content(self):
        self.test_user_token()
        url = drf_reverse('home')
        #(w,h)=(800,1280)
        #color = (255,255,255)
        image_item = Image.new('RGB',(800,1280),(0,124,174))
        temp_file=tempfile.NamedTemporaryFile(suffix='.jpg')
        image_item.save(temp_file,format='JPEG')

        with open(temp_file.name,'rb') as file_obj:

            data={
               # 'content':'some cool test content',
                'image':file_obj,
                }
            response=self.client.post(url,data,format='multipart') 
            self.assertEqual(response.status_code,status.HTTP_201_CREATED )
         #remove temp img
        temp_img_dir = os.path.join(settings.MEDIA_ROOT,'status','rahi')
        if os.path.exists(temp_img_dir):
            print('yes exists')
           
            shutil.rmtree(temp_img_dir)
    

    def test_status_create_and_get(self):
        data=self.create_item()
        data_id= data.get('id')
        rud_url = drf_reverse('status-detail',kwargs={'pk':data_id})
        rud_data={
            'content':'updated cool data'
        }

        #get method/ retrieve
        get_response=self.client.get(rud_url,foramt='json')
        self.assertEqual(get_response.status_code,status.HTTP_200_OK)
   
    def test_status_update(self):
        data=self.create_item()
        data_id= data.get('id')
        rud_url = drf_reverse('status-detail',kwargs={'pk':data_id})
        rud_data={
            'content':'updated cool data'
        }
        #put / update
        put_response=self.client.put(rud_url,rud_data,foramt='json')
        self.assertEqual(put_response.status_code,status.HTTP_200_OK)
        put_response_data=put_response.data
        self.assertEqual(put_response_data['content'],rud_data['content'])

    def test_status_delete(self):
        data=self.create_item()
        data_id= data.get('id')
        rud_url = drf_reverse('status-detail',kwargs={'pk':data_id})
        rud_data={
            'content':'updated cool data'
        }

        #delete method/delete
        delete_response=self.client.delete(rud_url,foramt='json')
        self.assertEqual(delete_response.status_code,status.HTTP_204_NO_CONTENT)
        
        #not found
        get_response=self.client.get(rud_url,foramt='json')
        self.assertEqual(get_response.status_code,status.HTTP_404_NOT_FOUND)
        


   
    def test_status_create_no_token(self):
        url = drf_reverse('home')
        data={'content':'some cool test content'}
        response=self.client.post(url,data,format='json') 
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED )
    
    def test_other_user_permission_api(self):
        data = self.create_item()
        data_id = data.get('id')
        user = User.objects.create(username='ice')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        rud_url = drf_reverse('status-detail',kwargs={'pk':data_id})
        rud_data = {
            'content':'blablablaa',
        }
        get_    = self.client.get(rud_url,format='json')
        put_    = self.client.put(rud_url,rud_data,format='json')
        delete_ =self.client.delete(rud_url,format='json')
        self.assertEqual(get_.status_code, status.HTTP_200_OK)
        self.assertEqual(put_.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_.status_code, status.HTTP_403_FORBIDDEN)