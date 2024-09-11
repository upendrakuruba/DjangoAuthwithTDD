# from django.test import TestCase
# from django.urls import reverse
# from authentication.models import  *
# from django.core import mail
# from django.contrib.messages import get_messages


# class BaseTest(TestCase):
#     def setUp(self):
#         self.register_url=reverse('register')
#         self.login_url=reverse('login')
#         self.home_url=reverse('home')
#         self.user={
#             'email':'testmail@gmail.com',
#             'first_name':'first_name',
#             'last_name':'last_name',
#             'password':'password',
#             'confirm_password':'password'


#         }
#         self.user1={
#             'email':'testmail@gmail.com',
#             'first_name':'first_name1',
#             'last_name':'last_name',
#             'password':'password',
#             'confirm_password':'password'


#         }
#         self.user_short_password={
#             'email':'testmail@gmail.com',
#             'first_name':'first_name',
#             'last_name':'last_name',
#             'password':'pas',
#             'confirm_password':'con'


#         }
#         self.user_unmathing_password={
#             'email':'testmail@gmail.com',
#             'first_name':'first_name',
#             'last_name':'last_name',
#             'password':'password',
#             'confirm_password':'passwordd'


#         }
#         self.user_invalid_email={
#             'email':'testcom',
#             'first_name':'first_name',
#             'last_name':'last_name',
#             'password':'password',
#             'confirm_password':'password'


#         }
#         return super().setUp()
    

# class RegisterTest(BaseTest):
#     def test_can_view_page_correctly(self):
#         response=self.client.get(self.register_url)
#         self.assertEqual(response.status_code,200)
#         self.assertTemplateUsed(response,'register.html')

#     def test_can_register_user(self):
#         response=self.client.post(self.register_url,self.user,format='text/html')
#         self.assertEqual(response.status_code,302)

#     def test_cant_register_user_withshortpassword(self):
#         response=self.client.post(self.register_url,self.user_short_password,format='text/html')
#         self.assertEqual(response.status_code,400)

#     def test_cant_register_user_with_unmatchingpassword(self):
#         response=self.client.post(self.register_url,self.user_unmathing_password,format='text/html')
#         self.assertEqual(response.status_code,400)


#     def test_cant_register_user_invalid_email(self):
#         response=self.client.post(self.register_url,self.user_invalid_email,format='text/html')
#         self.assertEqual(response.status_code,400)


#     def test_cant_register_user_taken_username(self):
#         self.client.post(self.register_url,self.user,format='text/html')
#         response=self.client.post(self.register_url,self.user,format='text/html')
#         self.assertEqual(response.status_code,400)

#     def test_cant_register_user_taken_email(self):
#         self.client.post(self.register_url,self.user1,format='text/html')
#         response=self.client.post(self.register_url,self.user,format='text/html')
#         self.assertEqual(response.status_code,400)

# class LoginTest(BaseTest):
#     def test_can_acess_page(self):
#         response=self.client.get(self.login_url)
#         self.assertEqual(response.status_code,200)
#         self.assertTemplateUsed(response,'login.html')

#     def test_login_success(self):
#         self.client.post(self.register_url,self.user1,format='text/html')
#         user=Account.objects.filter(email=self.user['email']).first()
#         user.is_active=True
#         user.save()
#         response=self.client.post(self.login_url,self.user1,format='text/html')
#         self.assertEqual(response.status_code,302)

#     def test_cant_login_with_unverified_email(self):
#         self.client.post(self.register_url,self.user1,format='text/html')
#         response=self.client.post(self.login_url,self.user1,format='text/html')
#         self.assertEqual(response.status_code,401)

#     def test_cantlogin_no_email(self):
#         response=self.client.post(self.login_url,{'email':'email@gmail.com','email':''},format='text/html')
#         self.assertEqual(response.status_code,401)

#     def test_cantlogin_no_password(self):
#         response=self.client.post(self.login_url,{'password':'password','password':''},format='text/html')
#         self.assertEqual(response.status_code,401)





# from django.test import TestCase
# from django.urls import reverse
# from authentication.models import *
# from rest_framework.test import APIClient

# class UserRegistrationTests(TestCase):

#     def setUp(self):
#         self.client = APIClient()

#     def test_successful_registration(self):
#         """Test that a user can register successfully with valid data"""
#         response = self.client.post(reverse('register'), {
#             'first_name': 'first_name',
#             'last_name': 'last_name',
#             'email': 'newuser@gmail.com',
#             'password': 'password',
#             'password': 'password',
#         })
#         self.assertEqual(response.status_code, 302)  # Redirect to login
#         self.assertTrue(Account.objects.filter(email='newuser@gmail.com').exists())

#     def test_username_uniqueness_real_time(self):
#         """Test real-time username availability check"""
#         User.objects.create_user(username='existinguser', email='test@example.com', password='password123')
#         response = self.client.post(reverse('validate_username'), {'username': 'existinguser'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['is_available'], False)

#     def test_email_uniqueness_real_time(self):
#         """Test real-time email availability check"""
#         User.objects.create_user(username='existinguser', email='existinguser@example.com', password='password123')
#         response = self.client.post(reverse('validate_email'), {'email': 'existinguser@example.com'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json()['is_available'], False)

#     def test_password_mismatch(self):
#         """Test that registration fails with mismatched passwords"""
#         response = self.client.post(reverse('register'), {
#             'username': 'newuser',
#             'email': 'newuser@example.com',
#             'password1': 'password123',
#             'password2': 'password456',
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertFormError(response, 'form', 'password2', "The two password fields didn’t match.")
