from django.test import TestCase
from django.contrib.auth import get_user, get_user_model
from django.conf import settings

User = get_user_model()
# Create your tests here.

class TestUserRegistration(TestCase):

    def setUp(self):
        user_a_username = 'miclem'
        self.username = user_a_username
        pas = 'Test123#'
        self.user_a_pass = pas
        user_a = User(username=self.username, email='mic@mail.com')
        user_a.set_password(self.user_a_pass)
        user_a.save()
        self.user = user_a

    def test_user_registration(self):
        qs = User.objects.filter(username='miclem')
        user = qs.first()
        print(user.username, user.email, user.password)
        self.assertEqual(qs.count(), 1)
        print(settings.LOGIN_URL)

    
    def test_user_login(self):
        # response = self.client.post(url, data, follow=True)
        data = {
            'username': self.username,
            'password': self.user_a_pass
        }
        response = self.client.post(settings.LOGIN_URL, data, follow=True)
        print(response.request)
        redirect_url = settings.LOGIN_REDIRECT_URL  
        path_redirect = response.request['PATH_INFO']
        self.assertEqual(redirect_url, path_redirect)
        status_code = response.status_code
        self.assertEqual(status_code, 200)

        # print(dir(response))

