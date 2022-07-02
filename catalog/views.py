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
    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)


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
        'product_objects': product_objects,
        'categories': categories,
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


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):

    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)


    customer = User.objects.get(person__id=pk)
    
    orders = customer.toyproduct_set.all()
    order_count = orders.count()

    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'product_objects': product_objects,
        'categories': categories,
    }
    return render(request, 'for_admin/customer.html', context)

@login_required(login_url='loginPage')
def userPage(request):

    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)

    user_products = request.user.toyproduct_set.all()
    
    context = {
        'user_products':user_products,
        'product_objects': product_objects,
        'categories': categories,
    }
    return render(request, 'account/user.html', context)

@login_required(login_url='loginPage')
def accountSettings(request):

    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)

    user = request.user.person
    form = CustomerForm(instance=user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('home'))
        else:
            print('Form is invalid.')
            return redirect('invalid')

    context = {
        'form':form,
        'product_objects': product_objects,
        'categories': categories,
    }
    return render(request, 'account/account_settings.html', context)


def category(request,pk):
    cat_id = Category.objects.get(id=pk)
    cat_name = cat_id.name
    req_category = request.GET.get('category')
    categories = Category.objects.all()

    toys = ToyProduct.objects.filter(category__name = cat_name)

    #paginator code 
    product_objects = ToyProduct.objects.filter(product_status = 'a')
    paginator = Paginator(product_objects, 6) #4 is changable!
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    context = {
        'cat_id': cat_id,
        'toys': toys,
        'req_category': req_category,
        'product_objects': product_objects,
        'categories': categories,
    }
    return render(request, 'category.html', context=context)  

def all_toys(request):
    categories = Category.objects.all()

    product_objects = ToyProduct.objects.all()
 
    #paginator code 
    product_objects = ToyProduct.objects.filter(product_status = 'a')
    paginator = Paginator(product_objects, 6) #4 is changable!
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    context = {
        'product_objects': product_objects,
        'categories': categories,
    }
    return render(request, 'all_toys.html', context=context)


def toy_slider(request):
    categories = Category.objects.all()

    product_objects = ToyProduct.objects.all()
 
    #paginator code 
    product_objects = ToyProduct.objects.filter(product_status = 'a')
    paginator = Paginator(product_objects, 6) #4 is changable!
    page = request.GET.get('page')
    product_objects = paginator.get_page(page)

    context = {
        'product_objects': product_objects,
        'categories': categories,
    }
    return render(request, 'slider.html', context=context)

  

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


def detail(request, pk):
    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        product_objects = ToyProduct.objects.filter(category__name = category)

    product_object = ToyProduct.objects.get(id=pk)
    num_comments = Comment.objects.filter(product=product_object).count()

    # Comment
    comments = Comment.objects.filter(product=product_object).order_by('date_added')
    
    # Comment form
    form = CommentForm(instance=product_object)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=product_object)
        if form.is_valid():
            name = request.user.username
            commenter = request.user
            body = form.cleaned_data['comment_body']

            c = Comment(product=product_object, commenter_name=name, commenter=commenter, comment_body=body, date_added=datetime.now())
            product_id = c.product.id
            c.save()
            return redirect(reverse('detail', args=[product_id]))
        else:
            print('Form is invalid.')
            return redirect('invalid')

    else:
        form = CommentForm()

    user = request.user.person

    context = {
        'product_object': product_object,
        'product_objects': product_objects,
        'categories': categories,
        'num_comments': num_comments,
        'comments': comments,
        'user': user,
    }
    return render(request, 'product/detail3.html', context=context)


def add_request(request, pk):
    product_object = ToyProduct.objects.get(id=pk)
    sender_toys = None

    sender_toys = ToyProduct.objects.filter(owner__username=request.user.username)

    form = RequestForm(instance=product_object)
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=product_object)

        if form.is_valid():
            user = request.user
            body = form.cleaned_data['notes']
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']


            form.save()
            #c = ToyRequest(sender=user, toy=product_object, notes=body, start_date=start, end_date=end)
            product_id =product_object.id
            #c.save()
            return redirect(reverse('detail', args=[product_id]))
        else:
            print('Form is invalid.')
            return redirect('invalid')

    else:
        form = RequestForm()

    context = {
        'product_object': product_object,
        'form': form,
        'sender_toys': sender_toys,
    }

    return render(request, 'product/add_toy_request.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def dashboard(request):

    category = request.GET.get('category')
    categories = Category.objects.all()

    if category == None:
        product_objects = ToyProduct.objects.all()
    else:
        #product_name__icontains=item_name
        product_objects = ToyProduct.objects.filter(category__name = category)


    customers = Person.objects.all() 
    orders = ToyProduct.objects.all()

    num_instances_available = ToyProduct.objects.filter(product_status__exact='a').count()
    num_instances_reserved = ToyProduct.objects.filter(product_status__exact='r').count()
    num_products = ToyProduct.objects.all().count()

    context = {
        'customers': customers,
        'orders': orders,
        'num_products': num_products,
        'num_instances_available': num_instances_available,
        'num_instances_reserved': num_instances_reserved,
        'product_objects': product_objects,
        'categories': categories,
    }
    return render(request, 'for_admin/dashboard.html', context=context)


@login_required(login_url='loginPage')
def addProduct(request, pk):
    owner = User.objects.get(id=pk)
    form = ProductForm(request.POST or None) 

    if request.method == 'POST': 
        if form.is_valid(): 
            toy = form.save(commit=False) 
            owner = User.objects.get(id = pk) 
            # you don't need to use this if statment 
            if owner: 
                toy.owner = owner 
                if toy.brand != None and toy.brand != 'Other':
                    toy.user_brand = toy.brand.name
                toy.save() 
                form.save_m2m()
                return redirect('/user')
        else:
            print('Form is invalid.')
            return redirect('invalid')
 
    context = {
        'form': form
    }
    return render(request, 'product/addProduct.html', context)


@login_required(login_url='loginPage')
def updateProduct(request, pk):
    product = ToyProduct.objects.get(id=pk)
    name = product.name

    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/category')
        else:
            print('Form is invalid.')
            return redirect('invalid')
        
    context = {
        'form': form,
        'name': name
    }
    return render(request, 'product/updateProduct.html', context)


@login_required(login_url='loginPage')
def deleteProduct(request, pk):
    product = ToyProduct.objects.get(id=pk)
    product.delete()
    return redirect('/category')


@login_required(login_url='loginPage')
def add_comment(request, pk):
    product_object = ToyProduct.objects.get(id=pk)
    product_commenter = request.user
    print(product_commenter)
    
    form = CommentForm(instance=product_object)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=product_object)
        if form.is_valid():
            name = request.user.username
            product_commenter = request.user
            body = form.cleaned_data['comment_body']

            c = Comment(product=product_object, commenter_name=name, commenter=product_commenter, comment_body=body, date_added=datetime.now())
            product_id = c.product.id
            c.save()
            return redirect(reverse('detail', args=[product_id]))
        else:
            print('Form is invalid.')
            return redirect('invalid')

    else:
        form = CommentForm()

    context = {
        'product_object': product_object,
        'form': form,
    }

    return render(request, 'product/add_comment.html', context)


@login_required(login_url='loginPage')
def delete_comment(request, pk):
    comment = Comment.objects.filter(product=pk).last()
    product_id = comment.product.id
    comment.delete()
    return redirect(reverse('detail', args=[product_id]))
