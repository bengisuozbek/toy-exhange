from django.db import models

from django.urls import reverse
import uuid
from django.conf import settings
from datetime import date
from django.contrib.auth.models import User

class Category(models.Model): # represents toy category
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, help_text='Enter a toy category')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class AgeInterval(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.name)

class Brand(models.Model):
    name = models.CharField(max_length=200,help_text="Enter the toy's brand")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(self.name)

class Person(models.Model):
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
    )

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(default='', max_length=255, unique=True)
    phone = models.CharField(max_length=100)   
    profile_pic = models.ImageField(default = "profile.png", null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('person-detail', args=[str(self.id)])

    def __str__(self):                  
        """String for representing the Model object."""
        return '{0}, {1}'.format(self.last_name, self.first_name)
  

class ToyProduct(models.Model):
    """Model representing a toy (but not a specific copy of a toy)."""
    name = models.CharField(max_length=200, unique=True, blank=False)

    # Foreign Key used because toy can only have one brand and age interval, but brands and age intervals can have multiple toys
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=False)
    age = models.ForeignKey(AgeInterval, on_delete=models.SET_NULL, null=True, blank=False)

    # ManyToManyField used because category can contain many toys. Toys can cover many categories.
    # Category class has already been defined so we can specify the object above.
    category = models.ManyToManyField(Category)

    image =  models.ImageField(default = "imageicon.png", null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 

    STATUS = (
        ('a', 'Available'),
        ('o', 'On loan'),
        ('r', 'Reserved')
    )

    product_status = models.CharField(
        max_length = 1,
        choices = STATUS,
        blank = True,
        default = 'a',
        help_text = 'Toy availability'
    )

    class Meta:
        ordering = ['name', 'age']
        permissions = (("can_mark_returned", "Set product as returned"),)

    def display_category(self):
        """Creates a string for the Category. This is required to display category in Admin."""
        return ', '.join([category.name for category in self.category.all()[:3]])
    
    display_category.short_description = 'Category'

    def __str__(self):
        """String for representing the Model object."""
        return str(self.id)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this toy product."""
        return reverse('product-detail', args=[str(self.name)])
        
class Comment(models.Model):
    product = models.ForeignKey(ToyProduct, related_name="comments", on_delete=models.CASCADE)
    commenter_name = models.TextField(max_length=400)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenter_user')
    comment_body = models.TextField(max_length=400)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.product.name, self.commenter_name)

class Contact(models.Model): # for support page!
    email = models.EmailField(blank=False)
    subject = models.CharField(max_length=250, blank=False)
    message = models.TextField(blank=False)

    def __str__(self):
        return self.email

class RequestforToy(models.Model):
    id = models.AutoField(primary_key=True)

    sender = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE, editable=False)
    sender_toy = models.ForeignKey(ToyProduct, on_delete=models.CASCADE, related_name='toyrequestsender')

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='toyrequestrecipient')
    requested_toy = models.ForeignKey(ToyProduct, on_delete=models.CASCADE, related_name='toyrequestborrow')

    notes = models.CharField(max_length=250, help_text="If you have something to add, you can write it here.")

    start_date = models.DateField(verbose_name="Start Date", help_text="Start date for toy is on ...", null=True, blank=False)
    end_date = models.DateField(verbose_name="End Date" , help_text="Coming back on ...", null=True, blank=False)

    is_accepted = models.BooleanField(default=False)
    is_ignored = models.BooleanField(default=False)

    class Meta:
        ordering = ['sender', 'sender_toy', 'requested_toy']

    def __str__(self):
        """String for representing the Model object."""
        return str(self.id)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this toy product."""
        return reverse('request-detail', args=[str(self.id)])