from django.shortcuts import render,redirect
from django.views.generic import View
from django.contrib import messages,auth
from validate_email import validate_email
from .models import *
# from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse

# Create your views here.

class RegistrationView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        if request.method == 'POST':
            context={'data':request.POST,'has_error':False}
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            username=first_name+' '+last_name
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
            send_email.send()
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
        return render(request,'home.html')
    



class LogoutView(View):
    def get(self,request):
        auth.logout(request)
        messages.success(request,'Successfully Logout')
        return redirect('login')