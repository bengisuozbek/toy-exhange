from django.shortcuts import render, redirect

from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from datetime import datetime
from price.decorators import unauthenticated_user, allowed_users, admin_only
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from catalog.models import *


# Create your views here.
@login_required(login_url='loginPage')
def inbox(request):
    the_user = request.user.id
    messages = Message.get_messages(the_user)
    other_users = User.objects.all()

    active_direct = None
    directs = None
    

    if messages:
        message = messages[0]
        active_direct = messages['user'].username
        directs = Message.objects.filter(user=request.user, recipient=message['user'])
        directs.update(is_read=True)

        for message in messages:
            if message['user'].username == active_direct:
                message['unread'] = 0

    num_users = User.objects.all().count()
    num_products = ToyProduct.objects.all().count()
    
    context = {
        'num_users': num_users,
        'num_products': num_products,
        'directs': directs,
        'messsages': messages,
        'active_direct': active_direct,
        'other_users': other_users,
    }
    
    return render(request, 'direct_message/direct_deneme.html', context)

@login_required(login_url='loginPage')
def directs(request, username):
    user = request.user.id
    messages = Message.get_messages(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0
    

    num_users = User.objects.all().count()
    num_products = ToyProduct.objects.all().count()


    context = {
        'num_users': num_users,
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
    }

    return render(request, 'direct_message/direct.html', context)



@login_required(login_url='loginPage')
def send_direct(request):
    from_user = request.user
    to_user_username = request.POST.get('to_user')
    body = request.POST.get('body')

    if request.method == 'POST':
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect('inbox')
    else:
        return redirect('index')


@login_required(login_url='loginPage')
def user_search(request):
    query = request.GET.get('q')
    context = {}

    if query:
        users = User.objects.filter(Q(username__icontains = query))

        #Pagination
        paginator = Paginator(users, 6)
        page_number = request.GET.get('page')
        users_paginator = paginator.get_page(page_number)

        context = {
            'users': users_paginator,
        }
    
    return render(request, 'direct_message/search_user.html', context)


@login_required(login_url='loginPage')
def new_conversation(request, username):
    from_user = request.user
    body = 'Says Hello!'

    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect('user_search')
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)
    return redirect('inbox')


@login_required(login_url='loginPage')
def searchbar_user(request):
    categories = Category.objects.all()

    other_users = User.objects.all()

    if request.method == 'GET':

        searched_objects_user_name = None
        searched_objects_first_name = None
        searched_objects_last_name = None


        search = request.GET.get('item_name')
        if search != '' and search is not None:
            searched_objects_user_name =  User.objects.all().filter(username__icontains=search) 
            searched_objects_first_name =  User.objects.all().filter(first_name__icontains=search)
            searched_objects_last_name =  User.objects.all().filter(last_name__icontains=search) 



    #category = request.GET.get('category')
    #categories = Category.objects.all()

    #if category == None:
    #    product_objects = ToyProduct.objects.all()
    #else:
    #    product_objects = ToyProduct.objects.filter(category__name = category)

    #product_object = ToyProduct.objects.get(id=pk)
    #num_comments = Comment.objects.filter(product=product_object).count()

    context = {
        'searched_objects_user_name': searched_objects_user_name,
        'searched_objects_first_name': searched_objects_first_name,
        'searched_objects_last_name': searched_objects_last_name,
        'categories': categories,
        'other_users': other_users,
    }
    return render(request, 'direct_message/searchbar_only_user.html', context=context)