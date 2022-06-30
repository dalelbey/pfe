from ast import Return
import json
from django.core import serializers
from multiprocessing import context
from pickle import TRUE
import re
from click import password_option
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from numpy import true_divide
from gfg import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from dashboard.views import index
from django.contrib.auth import get_user_model
import requests
from .models import Contact
from django.http import HttpResponse



User = get_user_model()
all_users = User.objects.all()

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")


def contact(request):
    if request.method == "POST":
       contact=Contact()
       name = request.POST.get('name')
       email = request.POST.get('email')
       subject = request.POST.get('subject')
       message = request.POST.get('message')
       contact.name=name
       contact.email=email
       contact.subject=subject
       contact.message=message
       contact.save()
       return HttpResponse("<h1>Your message has been sent. Thank you!</h1>")
    else :
        
        return  render(request, "authentication/contact.html") 

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        #myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to App Vesion!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to App Vesion \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        response = requests.post('https://api.emailjs.com/api/v1.0/email/send', headers={'origin':'http://localhost','Content-Type':'application/json'}, json = {'service_id':'service_hjs3nxi','template_id':'template_602laye', 'user_id':'CZsxM89l1uH1DnABd', 'template_params': {'name': fname , 'domain': current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(myuser.pk)), 'token': generate_token.make_token(myuser)}})
    
        response1 = requests.post('https://api.emailjs.com/api/v1.0/email/send', headers={'origin':'http://localhost','Content-Type':'application/json'}, json = {'service_id':'service_hjs3nxi','template_id':'template_0oer4hs', 'user_id':'CZsxM89l1uH1DnABd', 'template_params': {'name': fname , 'domain': current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(myuser.pk)), 'token': generate_token.make_token(myuser),  'user_email': myuser.email}})
    
        """
        email_subject = "Confirm your Email @ App Vesion!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        """
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')

""""""
def signin(request):
    all_users = User.objects.all()
    if request.method == 'POST':
        username = request.POST['email']
        pass1 = request.POST['pass1']
        #user_name = all_users[0]['username']
        #password = all_users[0]['password']
        
        #user = authenticate(username=username, password=pass1)
        #request.session['login'] = True 
        request.session['login'] = False
        request.session['user'] = ""
        active = 0
        for user in all_users:
            active = user.is_active
            if username ==user.get_username() and user.check_password(pass1):
                request.session['login'] = True
                request.session['user_id'] = user.id
                
                break

        if request.session['login']==True and active==1:
                return render(request,'dashboard/index.html', )
                
        else:
            return HttpResponse('bad credentials')
        """"
        if (username == user_name and pass1 == password):
            #login(request, user)
            #request.session['login'] = True
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return HttpResponse('logged in')#render(request, "dashboard/index.html",{"fname":fname,}) #{"fname":fname,})
        else:
            messages.error(request, "Bad Credentials!!")
            return HttpResponse(f'bad credentials {password}')#redirect('home')"""
    
    return render(request, "authentication/signin.html")


def signout(request):
    try:
         request.session['login']=False
    except KeyError:
        pass
    
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

    
def user_login(request):
    context = {

    }
    return render(request, "login/index.html")

def dashbord(request):
    if request.user.is_authenticated:
        request.session['login']= True
        return render(request, "dashborad/index.html")
    else:
        return HttpResponseRedirect("/login")

"""

def dashboard(request):
    if request.user.is_authenticated:
        return render(request, "dashborad/index.html")
    else:
        return HttpResponseRedirect("/login")
"""
def search(request):
    search = request.GET['search']
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')
    