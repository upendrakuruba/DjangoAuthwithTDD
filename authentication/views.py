from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib import messages,auth
from validate_email import validate_email
from .models import *
# from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.db import IntegrityError
from django.http import HttpResponse, Http404
from django.http import HttpResponseNotFound

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

import threading
# Create your views here.


class EmailThread(threading.Thread):
    def __init__(self,send_email):
        self.send_email = send_email
        threading.Thread.__init__(self)

    def run(self):
        self.send_email.send()


class RegistrationView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        if request.method == 'POST':
            context={'data':request.POST,'has_error':False}
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            username=request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if len(password)<6:
                messages.error(request,'Password should be at least 6 characters')
                context['has_error']=True
                return render(request,'register.html',context,status=400)
                
            if password != confirm_password:
                messages.error(request,'Password mismatch')
                context['has_error']=True
                return render(request,'register.html',context,status=400)  
        
                
            if not validate_email(email):
                messages.error(request,'Enter a valid email ')
                context['has_error']=True
                return render(request,'register.html',context,status=400)

            # if not username:
            #     messages.error(request,'Username require')
            #     context['has_error']=True
            #     return render(request,'register.html',context)

            if Account.objects.filter(username=username).exists():
                messages.error(request,'Username Token')
                context['has_error']=True
                return render(request,'register.html',context,status=400)

            if Account.objects.filter(email=email).exists():
                messages.error(request,'Email Token')
                context['has_error']=True
                return render(request,'register.html',context,status=400)
            
            if context['has_error']:
                return render(request,'register.html',context,status=400)
            
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.save()
            curren_site = get_current_site(request)
            email_subject = 'Please activate your account'
            message = render_to_string("account_verification_email.html",{
                'user':user,
                'domain':curren_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(email_subject,message,to=[to_email])
            # send_email.send()
            EmailThread(send_email).start()
            messages.success(request,'Account Created Successfully Please verify your email')
            return redirect('login')
        return render(request,'register.html',context)


def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations Your Account Activated')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    



class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    
    def post(self,request):
        if request.method == 'POST':
            context={'data':request.POST}
            email = request.POST.get('email')
            password = request.POST.get('password')

            if email == '':
                messages.error(request,'Email is required')

            if password == '':
                messages.error(request,'Password is required')

            user = auth.authenticate(email=email,password=password)
            
            if user is not None:
                auth.login(request,user)
                # messages.success(request,'Your now Logged in')
                return redirect('home')
            else:
                messages.error(request,'Email or Password not match')
                return render(request,'login.html',context,status=401)           
        return render(request,'login.html')
    

class HomeView(View):
    def get(self,request):
        try:
            if  UserProfile.objects.filter(user=request.user).exists():
                userprofile = UserProfile.objects.get(user=request.user)
                if request.method == 'POST':
                    pe_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
                    if pe_form.is_valid():
                        profile_form=pe_form.save()
                        messages.success(request,'Your profile has been updated')
                        return redirect('edit_profile')
                    else:
                        messages.error(request,'Your dont have a Account Please create')
                        return redirect('create_profile')
                else:
                    profile_form = UserProfileForm(instance=userprofile)
                context = {
                    'profile_form':profile_form,
                    'userprofile':userprofile,
                }
                return render(request,'home.html',context)
            else:
                messages.error(request,'Your not created profile Please create')
                return render(request,'user_not_login_home.html')
        except IntegrityError:
            return redirect('create_profile')


class LogoutView(View):
    def get(self,request):
        auth.logout(request)
        messages.success(request,'Successfully Logout')
        return redirect('login')
    

class RequestResetEmail(View):
    def get(self,request):
        return render(request,'forgotpassword.html')
    def post(self,request):
        if request.method == 'POST':
            email = request.POST.get('email')
            if Account.objects.filter(email=email).exists():
                user = Account.objects.get(email__exact=email)
                curren_site = get_current_site(request)
                email_subject = 'Reset Your Password'
                message = render_to_string("reset_password_email.html",{
                    'user':user,
                    'domain':curren_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(email_subject,message,to=[to_email])
                # send_email.send()
                EmailThread(send_email).start()
                messages.success(request,'Password Reset email has been sent to your address .')
                return redirect('login')
            else:
                messages.error(request,'Account does not exit')
                return redirect('forgotpassword')
        return render(request,'forgotpassword.html')
            


def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')
    


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password Reset Successfull')
            return redirect('login')
        else:
            messages.error(request,'Password do not match')
            return redirect('resetpassword')
    else:
        return render(request,'resetpassword.html')


@login_required(login_url='login')
def Edit_profile(request):
    try:
        if  UserProfile.objects.filter(user=request.user).exists():
            userprofile = UserProfile.objects.get(user=request.user)
            if request.method == 'POST':
                ur_form = UserForm(request.POST,instance=request.user)
                pe_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
                if ur_form.is_valid() and pe_form.is_valid():
                    user_form=ur_form.save()
                    profile_form=pe_form.save()
                    messages.success(request,'Your profile has been updated')
                    return redirect('edit_profile')
                else:
                    print('10------------------',ur_form.errors,pe_form.errors)
                    messages.error(request,'Your dont have a Account Please create')
                    return redirect('create_profile')
            else:
                user_form = UserForm(instance=request.user)
                profile_form = UserProfileForm(instance=userprofile)
            context = {
                'user_form':user_form,
                'profile_form':profile_form,
                'userprofile':userprofile,
            }
            return render(request,'edit_profile.html',context)
        else:
            messages.error(request,'Your not created profile Please create')
            return redirect('create_profile')
    except IntegrityError:
        return redirect('create_profile')









@login_required(login_url='login')
def create_profile(request):
    try:
        profile = request.user
    except UserProfile.DoesNotExist:
     profile = UserProfile(user=request.user)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                user = request.user
                profile_picture = form.cleaned_data['profile_picture']
                role = form.cleaned_data['role']
                country = form.cleaned_data['country']
                address_line_1 = form.cleaned_data['address_line_1']
                address_line_2 = form.cleaned_data['address_line_2']
                zipcode = form.cleaned_data['zipcode']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                mobile = form.cleaned_data['mobile']
                user = UserProfile(user=user,profile_picture=profile_picture,role=role,address_line_1=address_line_1,address_line_2=address_line_2,mobile=mobile,country=country,city=city,zipcode=zipcode,state=state)
                user.save()
                messages.success(request,' Your Profile Created .')
                return redirect('dashboard')
            except IntegrityError:
                messages.error(request,'Your already created profile')
                return redirect('edit_profile')

    else:
        form = CustomerProfileForm()
    context = {'form':form,'profile':profile}
    return render(request,'create_profile.html',context)


@login_required(login_url='login')
def DeleteView(request):
    try:
        userprofile = UserProfile.objects.get(user=request.user)
        userprofile.delete()
        messages.success(request,'Your profile deleted')
        return render(request,'user_not_login_home.html')
    except Exception as e:
        messages.error(request,'Your not created profile Please create')
        return redirect('create_profile')
@login_required(login_url='login')  
def Dashboard(request):
    try:
        if  UserProfile.objects.filter(user=request.user).exists():
            userprofile = UserProfile.objects.get(user=request.user)
            if request.method == 'POST':
                pe_form = UserProfileForm(request.POST,request.FILES,instance=userprofile)
                if pe_form.is_valid():
                    profile_form=pe_form.save()
                    messages.success(request,'Your profile has been updated')
                    return redirect('edit_profile')
                else:
                    messages.error(request,'Your dont have a Account Please create')
                    return redirect('create_profile')
            else:
                profile_form = UserProfileForm(instance=userprofile)
            context = {
                'profile_form':profile_form,
                'userprofile':userprofile,
            }
            return render(request,'dashboard.html',context)
        else:
            messages.error(request,'Your not created profile Please create')
            return render(request,'user_not_login_home.html')
    except IntegrityError:
        return redirect('create_profile')


@login_required(login_url='login')
def ChangePassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            succuss = user.check_password(current_password)
            if succuss:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password updated successfully')
                return redirect('changepassword')
            else:
                messages.error(request,'Please enter valid current password')
                return redirect('changepassword')
        else:
            messages.error(request,'Password does not match')
            return redirect('changepassword')

    return render(request,'changepassword.html')

# from django.db import IntegrityError
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import UserProfile
# from .forms import UserProfileForm

# def create_user_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#             try:
#                 form.save()
#                 return redirect('success_url')  # Replace with your success URL
#             except IntegrityError:
#                 return render(request, 'error_page.html', {'error': 'User ID already exists.'})
#     else:
#         form = UserProfileForm()
    
#     return render(request, 'create_user_profile.html', {'form': form})
