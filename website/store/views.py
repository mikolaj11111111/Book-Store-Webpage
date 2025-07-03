from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django import forms
from payment.forms import ShippingForm
from payment.models import ShippingAddress
import json
from cart.cart import Cart

def sell(request):
    categories = Category.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        description = request.POST.get('description')

        if name and price and category_id and image:
            # Pobranie obiektu kategorii
            category = Category.objects.get(id=category_id)
            current_user = User.objects.get(id=request.user.id)
            # Tworzenie nowego produktu
            Product.objects.create(
            name=name,
            price=price,
            category=category,
            description=description,
            image=image

            )
            return redirect('home')
        else:
            messages.error(request, "Fill the item info again")
    return render(request, 'sell.html', {'categories': categories})
"""
def sell(request):
    categories = Category.objects.all()
    form = SellInfoForm()
    if request.method == "POST":
        form = SellInfoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Item Added"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error with your item"))
            return redirect('sell')
    else:
        return render(request, 'sell.html', {'form': form, 'categories': categories})
"""

def search(request):
    #Check if the form is filled
    if request.method == 'POST':
        searched = request.POST['searched']
        #Query products in DB
        searched = Product.objects.filter(name__icontains=searched)
        if not searched:
            messages.success(request, "We don't have this product")
            return render(request, 'search.html',{})
        else:
            return render(request, 'search.html',{'searched':searched})
    else:
        return render(request, 'search.html',{})

def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None,instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()

            messages.success(request, "Info updated")
            return redirect('home')
        return render(request, 'update_info.html',{'form':form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == "POST":
            form = UpdateUserPassword(current_user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "PASSWORD UPDATED")
                login(request, current_user)
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = UpdateUserPassword(current_user)
            return render(request, 'update_password.html',{'form':form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserProfile(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "UPDATED")
            return redirect('home')
        return render(request, 'update_user.html',{'user_form':user_form})
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')


# Create your views here.
def category(request, foo):
    #x = x.replace('-', ' ')
    #Get the category name from url
    categories = Category.objects.all()
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        messages.success(request, ("udalo sie"))
        return render(request, 'category.html', {'products': products, 'category':category, 'categories': categories})
    except:
        messages.success(request, ("That category doesnt exit"))
        return redirect('home')
        
def product(request, pk):
    categories = Category.objects.all()
    product = Product.objects.get(id=pk)
    num_to_loop = range(1,10)
    return render(request, 'product.html', {'product':product, 'categories': categories, 'num_to_loop':num_to_loop})

def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products, 'categories': categories})

def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories': categories})


def login_user(request):
    categories = Category.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username, password=password)
        if user is not None:
            login(request, user)

            current_user = Profile.objects.get(user__id=request.user.id)
            #Get user saved cart form DB
            saved_cart = current_user.old_cart
            #Convert DB string into python dic
            if saved_cart:
                #Convert to dic using json
                converted_cart = json.loads(saved_cart)
                #Add loaded cart dic to the session
                cart = Cart(request)

                for key,value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
            messages.success(request, ("You have been logged in"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error"))
            return redirect('login')
    else:
        return render(request, 'login.html', {'categories': categories})


def logout_user(request):
    logout(request)
    messages.success(request, ("Thanks for visiting webiste. See you soon!"))
    return redirect('home')

def register_user(request):
    categories = Category.objects.all()
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            #login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect('update_info')
        else:
            messages.success(request, ("There was an error with your registration"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form, 'categories': categories})
    
