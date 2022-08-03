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

    image =  models.ImageField(default = "imageicon.png", upload_to="static/images/uploads", null=True, blank=True)
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


""" Toy Request (continue...) """
class ToyRequestList(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="owner") 
    toy_from_owner = models.OneToOneField(ToyProduct, on_delete=models.CASCADE, related_name='toy_from_owner')
    
    borrower = models.ManyToManyField(User)
    toy_from_borrower = models.OneToOneField(ToyProduct, on_delete=models.CASCADE, related_name='toy_from_borrower')

    def __str__(self):
        return self.toy_from_owner.id
    
    def display_borrower(self):
        """Creates a string for the Borrower. This is required to display borrower in Admin."""
        return ', '.join([user.username for user in self.borrower.all()[:3]])
    
    display_borrower.short_description = 'Borrower'

""" Toy Request (continue...) """
class ToyRequest(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE) 
    sender_toy = models.ForeignKey(ToyProduct, on_delete = models.CASCADE, null = False, related_name="sender_toy") 
   
    toy = models.OneToOneField(ToyProduct, on_delete = models.CASCADE, null = False, related_name="owner_toy") 
   
    notes = models.CharField(max_length=250, help_text="If you have something to add, you can write it here.")

    start_date = models.DateField(verbose_name="Start Date", help_text="Start date for toy is on ...", null=True, blank=False)
    end_date = models.DateField(verbose_name="End Date" , help_text="Coming back on ...", null=True, blank=False)

    status = models.CharField(max_length=12, default="Pending") #Pending, Approved, Rejected, Cancelled
    is_approved = models.BooleanField(default=False)

    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __str__(self):
        return '%s - %s' % (self.toy.name, self.person.user.username)

    def calling_user(self):
        return self.toy.user.username
    
    def accept(self):
        # SWAPPING THE TOYS
        """
            Accept a toy request
            Update both SENDER and TOY toy request lists
        """ 
        # received_request_list = ToyRequestList.objects.get(toy_from_owner = self.toy)
        # if received_request_list:
        #     received_request_list.add_toy_request(self.sender)
        #     sender_request_list = ToyRequestList.objects.get(toy_from_borrower = self.sender_toy)
        #     if sender_request_list:
        #         sender_request_list.add_toy_request(self.toy.person)    
        #         self.status = "Approved"
        #         self.save()

        owner_toy = ToyRequestList.objects.get(toy_from_owner = self.toy)

        if owner_toy:
            sender_toy = ToyRequestList.objects.get(toy_from_borrower = self.sender_toy)
            if sender_toy:
                self.status = "Approved"
                self.toy_from_owner.product_status = "r"
                self.toy_from_borrower.product_status = "r"

                self.save()
    
    def decline(self):
        """
            Decline a toy request.
            It is declined by setting the 'is_active' field to False
        """
        self.status = "Rejected"
        self.save()
    
    def cancel(self):
        """
            Cancel a toy request
            It is 'cancelled' by setting the 'is_active' field to False.
            This is only different with respect to "declining" through the notification
            that is generated.
        """
        self.status = "Canceled"
        self.save()

    @property
    def is_overdue(self):
        if self.end_date and date.today() > self.end_date:
            return True
        return False


class Contact(models.Model): # for support page!
    email = models.EmailField(blank=False)
    subject = models.CharField(max_length=250, blank=False)
    message = models.TextField(blank=False)

    def __str__(self):
        return self.email
        

class ProductRequest(models.Model):
    id = models.AutoField(primary_key=True)

    sender = models.ForeignKey(User, null=True, blank=False, on_delete=models.CASCADE, editable=False)
    sender_toy = models.ForeignKey(ToyProduct, on_delete=models.CASCADE, related_name='requestsender')

    requested_toy = models.OneToOneField(ToyProduct, on_delete=models.CASCADE, related_name='requestborrow')

    notes = models.CharField(max_length=250, help_text="If you have something to add, you can write it here.")

    start_date = models.DateField(verbose_name="Start Date", help_text="Start date for toy is on ...", null=True, blank=False)
    end_date = models.DateField(verbose_name="End Date" , help_text="Coming back on ...", null=True, blank=False)

    class Meta:
        ordering = ['sender', 'sender_toy', 'requested_toy']

    def __str__(self):
        """String for representing the Model object."""
        return str(self.id)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this toy product."""
        return reverse('request-detail', args=[str(self.id)])