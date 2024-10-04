from django.shortcuts import render,redirect
from .models import Product,Category
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django import forms
from .forms import UserRegistrationForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
User=get_user_model()

# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user =form.save()
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            # login(request, user) 
            return redirect('login_cus')
    else:
        form = UserRegistrationForm()
    return render(request, 'register_cus.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request,username=username, password=password)
        if user is not None:
            if user.is_superuser:  # Check if the user is an admin
                login(request, user)
                return redirect('/admin/') 
            elif user.is_staff:
                login(request, user)
                request.session['username']=username
                user=username
                return redirect('home')
            else:
                login(request, user)
                return redirect('login_cus')
        else:
            # Authentication failed
            return render(request,'login_cus.html')

    return render(request, 'login_cus.html')

def logout_view(request):
    logout(request)
    return redirect('home') 

def topoffers(request):
    prd=Product.objects.all()
    return render(request,'topoffers.html',{ 'prd':prd })


def homenew(request):
    prd=Product.objects.all()
    # print('you are',request.session.get('username'))
    # p=Paginator(Product.objects.all(),10)
    # page=request.GET.get('page')
    # prds=p.get_page(page)
    return render(request,'index.html',{ 'prd':prd})

def productpage(request,pk):
    prd=Product.objects.get(id=pk)
    return render(request,'product.html',{ 'prd':prd })


def category_view(request,pk):
    if(Category.objects.filter(id=pk)):
        prd=Product.objects.filter(category__id=pk)
        cat=Category.objects.filter(id=pk).first()
        context={
        'prd':prd,
        'cat':cat
        }
        return render(request,'categoryproducts.html',context)
    else:
        messages.warning(request,'No such Category found')
        return redirect(request, 'categorylist.html')

def categorylist(request):
    cat=Category.objects.all()
    return render (request, 'categorylist.html',{ 'cat':cat})

