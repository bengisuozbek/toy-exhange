from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['phone']

class ProductForm(ModelForm):
    # categories = forms.ModelMultipleChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    class Meta:
        model = ToyProduct
        fields = ['name', 'brand', 'age', 'category', 'image', 'description']
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_body']
        widgets = {
            'comment_body': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone', 'profile_pic']
    
class DateInput(forms.DateInput):
    input_type = 'date'

class RequestForm(forms.ModelForm):
    class Meta:
        model = ProductRequest
        fields = ['start_date', 'end_date', 'notes', 'sender_toy']
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'start_date': DateInput,
            'end_date': DateInput
        }

       
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'