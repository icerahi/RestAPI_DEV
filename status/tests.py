from django.test import TestCase

from django.contrib.auth import get_user_model

User = get_user_model()

class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='rahi',email='rahi@gmail.com')
        user.set_password('rahirahi')
        user.save() 


    def test_created_user(self):
        qs = User.objects.filter(username='rahi')
        self.assertEqual(qs.count(),1)