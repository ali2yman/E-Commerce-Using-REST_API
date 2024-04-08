from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver 
from django.db.models.signals import post_save
# Create your models here.




class Profile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50,default="",blank=True)               #to store a token for password reset
    reset_password_expire = models.DateTimeField(null=True,blank=True)                         #to store the expiry date/time for the password reset token
 




@receiver(post_save, sender=User)                         # @receiver >>> decorator used to register a function 
def save_profile(sender,instance, created, **kwargs):

    print('instance',instance)
    user = instance

    if created:
        profile = Profile(user = user)
        profile.save()
     


# this code ensures that every time a new User instance is created, a corresponding Profile instance is also created and associated with it. 
# This is achieved by listening to the post_save signal emitted by the User model and responding accordingly in the save_profile function.