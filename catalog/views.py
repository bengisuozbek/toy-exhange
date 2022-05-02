from django.shortcuts import render, redirect

# Create your views here.
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
from django.views import generic

from .forms import ContactForm, CreateUserForm, ProductForm, CommentForm, CustomerForm, RequestForm
from .models import *
from catalog.decorators import unauthenticated_user, allowed_users, admin_only

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_toy = ToyProduct.objects.all().count()

    # Available books (status = 'a')
    #num_instances_available = ToyProduct.objects.filter(status__exact='a').count()

    # num of visitors 
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_toy': num_toy,
        'num_visits': num_visits,
    }

    return render(request, 'main/index.html', context=context)

def invalid(request):

    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)

    #paginator code 
    paginator = Paginator(product_objects, 8) #4 is changable!
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    context = {
        'product_objects': product_objects,
        'categories': categories,
    }

    return render(request, 'invalid.html', context=context)

@unauthenticated_user
def register(request):

    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)
    
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
            
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('loginPage')
        else:
            print('Form is invalid.')
            return redirect('invalid')

    context = {
        'form':form,
        'product_objects': product_objects,
        'categories': categories,
    }
    return render(request, 'registration/register.html', context)

@unauthenticated_user
def loginPage(request):

    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect.')

    context = {
        'product_objects': product_objects,
        'categories': categories,
    }
    return render(request, 'registration/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
def home(request):

    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)

    # user = request.user.id
    # request_list = ToyRequestList.objects.get(owner=user)

    context = {
        'product_objects': product_objects,
        'categories': categories,
        # 'request_list': request_list,
    }
    return render(request, 'registration/home.html', context)

def support(request):
    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)

    #paginator code 
    paginator = Paginator(product_objects, 8) #4 is changable!
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():

            user_mail = request.user.person.email
            if user_mail:
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']

                body = message + "\nSender's email: "+ user_mail

                send_mail(subject, body, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL, fail_silently=False)
            else:
                subject = form.cleaned_data['subject']
                from_email = form.cleaned_data['from_email']
                message = form.cleaned_data['message']

                body = message + "\nSender's email: "+ from_email

                send_mail(subject, body, settings.CONTACT_EMAIL, settings.ADMIN_EMAIL, fail_silently=False)
          
            return render(request, 'support/contact_success.html')   
        else:
            print('Form is invalid.')
            return redirect('invalid')

    form = ContactForm()

    context = {
        'product_objects': product_objects,
        'categories': categories,
        'form': form,
    }
    return render(request, 'support/support.html', context=context)

def searchbar(request):
    categories = Category.objects.all()

    if request.method == 'GET':

        searched_objects_name = None
        searched_objects_brand = None
        searched_objects_age = None
        searched_objects_category = None

        search = request.GET.get('item_name')
        if search != '' and search is not None:
            searched_objects_name =  ToyProduct.objects.all().filter(name__icontains=search) 
            searched_objects_brand =  ToyProduct.objects.all().filter(brand__name__icontains=search)
            searched_objects_age =  ToyProduct.objects.all().filter(age__name__icontains=search)
            searched_objects_category =  ToyProduct.objects.all().filter(category__name__icontains=search)

    #category = request.GET.get('category')
    #categories = Category.objects.all()

    #if category == None:
    #    product_objects = ToyProduct.objects.all()
    #else:
    #    product_objects = ToyProduct.objects.filter(category__name = category)

    #product_object = ToyProduct.objects.get(id=pk)
    #num_comments = Comment.objects.filter(product=product_object).count()

    context = {
        'searched_objects_name': searched_objects_name,
        'searched_objects_brand': searched_objects_brand,
        'searched_objects_age': searched_objects_age,
        'searched_objects_category': searched_objects_category,
        'categories': categories,
    }
    return render(request, 'main/searchbar.html', context=context)