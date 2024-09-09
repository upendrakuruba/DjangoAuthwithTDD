from django.test import TestCase
from django.urls import reverse
from authentication.models import  *
class BaseTest(TestCase):
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.home_url=reverse('home')
        self.user={
            'email':'testmail@gmail.com',
            'first_name':'first_name',
            'last_name':'last_name',
            'password':'password',
            'confirm_password':'password'


        }
        self.user1={
            'email':'testmail@gmail.com',
            'first_name':'first_name1',
            'last_name':'last_name',
            'password':'password',
            'confirm_password':'password'


        }
        self.user_short_password={
            'email':'testmail@gmail.com',
            'first_name':'first_name',
            'last_name':'last_name',
            'password':'pas',
            'confirm_password':'con'


        }
        self.user_unmathing_password={
            'email':'testmail@gmail.com',
            'first_name':'first_name',
            'last_name':'last_name',
            'password':'password',
            'confirm_password':'passwordd'


        }
        self.user_invalid_email={
            'email':'testcom',
            'first_name':'first_name',
            'last_name':'last_name',
            'password':'password',
            'confirm_password':'password'


        }
        return super().setUp()
    

class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response=self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'register.html')


    def test_can_register_user(self):
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,302)

    def test_cant_register_user_withshortpassword(self):
        response=self.client.post(self.register_url,self.user_short_password,format='text/html')
        self.assertEqual(response.status_code,400)

    def test_cant_register_user_with_unmatchingpassword(self):
        response=self.client.post(self.register_url,self.user_unmathing_password,format='text/html')
        self.assertEqual(response.status_code,400)


    def test_cant_register_user_invalid_email(self):
        response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
        self.assertEqual(response.status_code,400)


    def test_cant_register_user_taken_username(self):
        self.client.post(self.register_url,self.user,format='text/html')
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,400)

    def test_cant_register_user_taken_email(self):
        self.client.post(self.register_url,self.user1,format='text/html')
        response=self.client.post(self.register_url,self.user,format='text/html')
        self.assertEqual(response.status_code,400)


class LoginTest(BaseTest):
    def test_can_acess_page(self):
        response=self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'login.html')

    def test_login_success(self):
        self.client.post(self.register_url,self.user1,format='text/html')
        user=Account.objects.filter(email=self.user['email']).first()
        user.is_active=True
        user.save()
        response=self.client.post(self.login_url,self.user1,format='text/html')
        self.assertEqual(response.status_code,302)

    def test_cant_login_with_unverified_email(self):
        self.client.post(self.register_url,self.user1,format='text/html')
        response=self.client.post(self.login_url,self.user1,format='text/html')
        self.assertEqual(response.status_code,401)

    def test_cantlogin_no_email(self):
        response=self.client.post(self.login_url,{'email':'email@gmail.com','email':''},format='text/html')
        self.assertEqual(response.status_code,401)


    def test_cantlogin_no_password(self):
        response=self.client.post(self.login_url,{'password':'password','password':''},format='text/html')
        self.assertEqual(response.status_code,401)


class HomeTest(BaseTest):
   def test_can_acess_page(self):
        response=self.client.get(self.home_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'home.html')


    



    



    

