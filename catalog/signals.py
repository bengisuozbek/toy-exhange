from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.contrib.auth.models import User, Group  # Required to assign User as a borrower
from .models import Person

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)

        Person.objects.create(
            user=instance,
            first_name = instance.first_name,
            last_name = instance.last_name,
            email = instance.email,
        )

        print('Profile created!')
    
    #post_save.connect(create_profile, sender=User)

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.person.save()
        #print('Profile updated!')
    
    #post_save.connect(update_profile, sender=User)