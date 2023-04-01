

from django.contrib.auth.models import User ,auth
from django.contrib import messages
from b_app.models import Person,ContactUs
from b_app.forms import Blogform,Contactform
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



from django.shortcuts import redirect, render

# Create your views here.
def home(request):
    blogs_list = Person.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(blogs_list, 6)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render(request,'home.html',{'blogs':blogs})

def exit(request):
    return render(request,'base.html')

def index(request):
    user_list = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 2)
    try:
        
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'home.html', { 'users': users })

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name'] 
        last_name= request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username all ready taken !!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email all ready taken !!')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name, last_name= last_name,username=username,email=email,password=password1)
                user.save()
                return redirect('login')
        else: 
            messages.info(request,'Password not matching!!')    
            return redirect('register')
    else:
        return render(request,'register.html')
def login (request):
    if request.method=='POST':
        username=request.POST['username']
        password= request.POST['password']
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'user is not valid!!')
    else:
        return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return redirect('login')
    
def bgregister(request):
    if request.method=='GET':
        formm=Blogform()
        return render(request,'blog_reg.html',{'form':formm})   
    else:
        form=Blogform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')     


def changepassword(request):
    if request.method == "GET":#get request for rendring changepass html page
        ss = PasswordChangeForm(user=request.user) 
        return render(request,'changepass.html',{'form':ss})

    elif request.method  == "POST":
        aa = PasswordChangeForm(user=request.user,data=request.POST)#post data in database
        if aa.is_valid():
            userr=aa.save()
            update_session_auth_hash(request,userr)
            return redirect('home')



@login_required(login_url='login')
def update(request,id):
    if request.method == 'POST':
        student = Person.objects.get(id=id)
        print(student)
        form = Blogform(request.POST,request.FILES,instance=student)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        student = Person.objects.get(id=id)
        form = Blogform(instance=student)
        return render(request,'update.html',{'form':form})


def Contact(request):
    if request.method=='GET':
        formm=Contactform()
        return render(request,'contactus.html',{'form':formm})   
    else:
        form=Contactform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')   

def contacts(request):
    a = ContactUs.objects.all()
    return render (request,'show.html',{'a':a})