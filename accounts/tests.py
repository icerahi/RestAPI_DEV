from django.test import TestCase

from django.contrib.auth import get_user_model
from status.models import Status
User = get_user_model()

class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='rahi',email='rahi@gmail.com')
        user.set_password('rahirahi')
        user.save() 


    def test_created_user(self):
        qs = User.objects.filter(username='rahi')
        self.assertEqual(qs.count(),1)

    def test_creating_status(self):
        user = User.objects.get(username='rahi')
        obj = Status.objects.create(user=user,content='new content test')
        self.assertEqual(obj.id,1)

        qs = Status.objects.all()
        self.assertEqual(qs.count(),1)