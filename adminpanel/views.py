from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import  reverse
from django.contrib import messages
from .forms import contactform, registerform,resetpasswordform,loginform,forgotpasswordform,profileform
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import  send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from adminpanel.models import post,profile, words
import pdb
import logging
def index(request):
    logger=logging.getLogger("testing")
    blogtitle="bjarath"
    posts=post.objects.all()
    logger.debug("Blog title: %s", blogtitle)
    print(blogtitle)
   
    
    

   
    
    return render(request,"index.html",{ 'blogtitle':blogtitle})
def index1(request):
    blogtitle="bjarath"
    posts=post.objects.all()
    return render(request,"index1.html",{ 'blogtitle':blogtitle,'posts':posts})
    

# Create your views here.
def register(request):
    form=registerform()
    blogtitle="bjarath" 
    if request.method =='POST':
        form=registerform(request.POST)
        if form.is_valid():

            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            """  print('registersucess') """
            messages.success(request,"registration succesfull")
            return redirect("login")
         
    
               
    return render (request,"register.html",{'form':form,'blogtitle':blogtitle})

def about(request):
    return render(request,'about.html')

def dyslexia(request):
     return render (request,"dyslexia.html")
def texttospeech(request):
    return render(request,'texttospeech.html')
def example(request):
    return render(request,'example.html')
def login(request):
    form=loginform()
    if request.method =="POST":
        form=loginform(request.POST)
        if form.is_valid():
           
           print("login success")
           username=form.cleaned_data['username']
           password=form.cleaned_data['password']
           user=authenticate(username=username,password=password)
           if user is not None:
            auth_login(request,user)
            messages.success(request,'you are successfully logged in')
            return redirect("index")
            
                
            
    return render (request,"login.html",{'form':form})
def logout(request):
    print("Logging out user")
    auth_logout(request)
    return redirect('login')
def forgotpassword(request):
    form=forgotpasswordform()
    if request.method=='POST':
        form=forgotpasswordform(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.get(email=email)
            #send resnt email
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            currentsite=get_current_site(request)
            domain=currentsite.domain
            subject="reset password requsted"
            message=render_to_string('resetpassword.html',{
                'domain':domain,
                'uid':uid,
                'token':token
            })
            send_mail(subject,message,'noreply@hellojiohellojio.com',[email])
            messages.success(request,"your email is sent")





        
    return render(request,'forgotpassword.html',{'form':form})
def resetpassword(request,uidb64,token):
    form=resetpasswordform()
    if request.method=='POST':
        form=resetpasswordform(request.POST)
        if form.is_valid():
            newpassword=form.cleaned_data['newpassword']
            try:
                uid=urlsafe_base64_decode(uidb64)
                user=User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None
            if user  is not None and default_token_generator.check_token(user,token):
                user.set_password(newpassword)  
                user.save()
                messages.success(request,'password changed correctly')    
                return redirect('login') 
            else:
                messages.error(request,'the password link is invalid')




    return render(request,'resetpassword2.html',{'form':form})

def game(request):
    return render (request,"game.html")
def index(request):
    return render(request,"index.html")
def profiles(request):
    posts=profile.objects.first()
    return render(request,"profile.html",{'posts':posts})
def game(request):
    # Fetch all the word posts
    posts = words.objects.all().values('name', 'image')  # Get 'name' and 'image' fields
    
    # Pass the serialized data to the template
    return render(request, "game.html", {'posts': list(posts), 'blogtitle': 'bjarath'})

def createprofile(request):
    form=profileform()
    if request.method=="POST":
        form=profileform(request.POST,request.FILES)
        if form .is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('profile')
    return render(request,"createprofile.html",{'form':form})

""" def newpost(request):
    
    form=profileform()
    if request.method=="POST":
        form=profileform(request.POST,request.FILES)
        if form .is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('adminpanel:dashboard')
    return render(request,'newpost.html',{'form':form}) """
def contact(request):
     form=contactform()
     if request.method=='POST':
        form=contactform( request.POST)
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        send_mail(name,message,'noreply@hellojiohellojio.com',[email])
        messages.success(request,"your email is sent")
     return render(request,'contact.html',{'form':form})  
def deepak(request):
    return render(request,'deepak.html')


