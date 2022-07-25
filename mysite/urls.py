"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from catalog import views


#    path('', TemplateView.as_view(template_name="index.html")),
#   For the above url, check the conditions! 

urlpatterns = [

    path('', TemplateView.as_view(template_name="index.html")),
    path('accounts/', include('allauth.urls')),

    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),

    path('admin/', admin.site.urls),
    path('index/', include('catalog.urls')),
    path('upload/', include('price.urls')),
    path('message/', include('message.urls')),

    path('home/', views.home, name='home'),

    path('allToys/', views.all_toys, name="all_toys"),
    path('privacy/', views.privacy, name="privacy"),
    path('category/<int:pk>/', views.category, name="category"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('support/', views.support, name="support"),

    path('searchbar/', views.searchbar, name="searchbar"),
    path('invalid/', views.invalid, name="invalid"),
    
    path('account/', views.accountSettings, name="account"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="loginPage"),
    path('logout/', views.logout_view, name="logout"),

    path('user/', views.userPage, name="user-page"),
    path('customer/<str:pk>/', views.customer, name='customer'),

    path('product/<int:pk>/', views.detail, name='detail'),
   
    path('addProduct/<int:pk>/', views.addProduct, name='addProduct'),
    path('updateProduct/<int:pk>/', views.updateProduct, name='updateProduct'),
    path('deleteProduct/<int:pk>/', views.deleteProduct, name='deleteProduct'),
        
    path('<int:pk>/add-comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/delete-comment/', views.delete_comment, name='delete_comment'),

    path('add_request/<int:pk>/', views.add_request, name='add_request'),

    path('', RedirectView.as_view(url='index/', permanent=True)),

    path('deneme/', views.deneme, name='deneme'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)