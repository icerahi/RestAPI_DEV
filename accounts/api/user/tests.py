from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as drf_reverse
from django.contrib.auth import get_user_model
from status.models import Status

from rest_framework import status 

User = get_user_model()

class UserAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='rahi',email='rahi@gmail.com')
        user.set_password('rahirahi')
        user.save() 


    def test_created_user(self):
        qs = User.objects.filter(username='rahi')
        self.assertEqual(qs.count(),1)

    def test_register_user_fail(self):
        url = drf_reverse('register')
        data = {
            'username':'rahis',
            'email':'rahid@gmail.com',
            'password':'rahirahi',
        }
        response = self.client.post(url,data,format='json')
        # print(dir(response))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password2'][0], 'This field is required.')


    def test_register_user_api(self):
        url = drf_reverse('register')
        data = {
            'username':'rahis',
            'email':'rahid@gmail.com',
            'password':'rahirahi',
            'password2':'rahirahi'
        }
        response = self.client.post(url,data,format='json')
        token_len = len(response.data.get('token',0))
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertGreater(token_len, 0)
    
    def test_login_user_api(self):
        url = drf_reverse('login')
        data = {
            'username':'rahi',
        
            'password':'rahirahi',
          
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data.get('token',0)
        token_len = 0
        if token !=0:
            token_len=len(token)        
        self.assertGreater(token_len, 0)

    def test_login_user_api_fail(self):
        url = drf_reverse('login')
        data = {
            'username':'rahi',
            'email':'rahid@gmail.com',
   
        }
        response = self.client.post(url,data,format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        token = response.data.get('token',0)
        token_len = 0
        if token !=0:
            token_len=len(token)  
        self.assertEqual(token_len, 0)

    def test_token_login_api(self):
        url = drf_reverse('login')
        data = {'username':'rahi','password':'rahirahi'}
        
        response = self.client.post(url,data,format='json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token',None)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        response2=self.client.post(url,data,format='json')
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)

    def test_token_register_user_api(self):
        url = drf_reverse('login')
        data = {'username':'rahi','password':'rahirahi'}
        
        response = self.client.post(url,data,format='json') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token',None)
        self.client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        
        url2 = drf_reverse('register')
        data2 = {
            'username':'rahis',
            'email':'rahid@gmail.com',
            'password':'rahirahi',
            'password2':'rahirahi'
        }
        response=self.client.post(url2,data2,format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 

        