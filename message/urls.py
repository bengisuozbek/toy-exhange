from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('directs/<username>/', views.directs, name='directs'),
    path('send/', views.send_direct, name='send_direct'),
    path('new/', views.user_search, name='user_search'),
    path('new/<username>/', views.new_conversation, name='new_conversation'),
    path('searchbarUser/', views.searchbar_user, name="searchbar_user"),
]