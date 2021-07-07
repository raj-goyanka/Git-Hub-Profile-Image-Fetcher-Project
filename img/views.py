#Imports
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import logout,login
import requests
from bs4 import BeautifulSoup as bs
from .models import Github
from django.conf import settings
from django.core.mail import send_mail
from .models import Profile
import uuid
from django.http import HttpResponseRedirect

#This Function is used to send Varification mail to User's Email. 
def email_sender(email,token,username):
    subject = 'Verify Email'
    message = f'''
      Hello , {username}
          You registered an account on GitHub Image Fetcher WebSite, before being able to use you account you need to verify that this is your email address by clicking here: http://127.0.0.1:8000/account_verify/{token}/
                  
          Kind Regards,Team Goyanka'''
    #Click On the Link to verify your account http://127.0.0.1:8000/account_verify/{token}/
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]
    send_mail(subject, message, email_from, recipient_list)

#This Function is used to Varify Users Email Varification Token. 
def account_verify(request,token):
    profile=Profile.objects.filter(token=token).first()
    profile.verify=True
    profile.save()
    messages.success(request,"Your account has been varified , You can LogIn Now")
    return HttpResponseRedirect('/user_signin/')

#This Funtion is used For Web Scraping From GitHub.
def index(request):
   if request.user.is_authenticated:
      if request.method == 'POST':
         github_user = request.POST['github_user']
         user = request.POST['user']
         url = 'https://github.com/'+github_user
         r = requests.get(url)
         soup = bs(r.content)
         tem="@"+github_user
         profile = soup.find('img', {'alt' :tem })['src']
         new_github = Github(
            githubuser = github_user,
            imagelink = profile,
            username = user
         )
         new_github.save()
         messages.info(request, 'User '+ github_user +' Image Saved')
         return redirect('/index/')
      else:
       return render(request, 'index.html')
   else:
        return redirect('/user_signin/')

#This is Signup Function.
def user_signup(request):
  if not request.user.is_authenticated:
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Taken')
                return redirect('/user_signup/')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Taken')
                return redirect('/user_signup/')
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()
                uid=uuid.uuid4()
                profile=Profile(user=new_user,token=uid)
                profile.save()
                email_sender(email,uid,username)
                messages.success(request,"Your Account Created Successfully , to Varify your Account Check Your Email !")
                return redirect('/user_signup/')
        else:
            messages.info(request, 'Password is Not Matching')
            return redirect('/user_signup/')
    else:
        return render(request, 'signup.html')
  else: 
      return user_signout(request)
         
#This is Signin Function.         
def user_signin(request):
  if not request.user.is_authenticated:
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            profile=Profile.objects.filter(user=user).first()           
            if profile.verify:
              auth.login(request, user)
              return HttpResponseRedirect('/index/')
            messages.info(request,"You are not varified , Check Your Gmail Account and varify yourself !")
            return redirect('/user_signin/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('/user_signin/')
    else:
        return render(request, 'login.html')
  else:
      return user_signout(request) 

#This is Signout Function.
def user_signout(request):
   if request.user.is_authenticated: 
     logout(request)
     return redirect('/user_signin/')
   else:
     return redirect('/user_signin/') 

#This Function is used to Display GitHub Users Images. 
def images(request):
   if request.user.is_authenticated:
     username = request.user
     git_hub = Github.objects.filter(username=username)
     return render(request, 'images.html', {'git_hub':git_hub})
   else:
      return redirect('/user_signin/') 

#This is Simply HomePage Function View.
def home(request):
    return render(request,'home.html')