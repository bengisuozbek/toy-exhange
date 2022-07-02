from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),

    path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name = "account/password_reset.html"), 
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name = "account/password_reset_sent.html"),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name = "account/password_reset_form.html"), 
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name = "account/password_reset_done.html"), 
        name="password_reset_complete"),

    # path('login/', auth_views.login, name='login'),
    # path('logout/', auth_views.logout, name='logout'),
    # path('oauth/', include('social_django.urls', namespace='social')),
    # path('admin/', admin.site.urls),
]