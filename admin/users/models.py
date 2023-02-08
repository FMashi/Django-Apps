import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
#from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html
from PIL import Image
from uuid import uuid4
from django.utils.deconstruct import deconstructible
from django.db.models.signals import post_save
from django.dispatch import receiver

@deconstructible
class PathRename(object):
    def __init__(self, sub_path):
        self.path = sub_path
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)


class User_Profile(models.Model):
    ROLES = [
        ('user', 'User'),
        ('customer', 'Customer'),
        ('author', 'Author'),
        ('editor', 'Editor'),
        ('manager', 'Manager'),
        ('support', 'Support'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User,related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField(blank=True) 
    image = models.ImageField(default='person.png', upload_to=PathRename('images/users'))
    birthday = models.DateField(null=True, blank=True) 
    join_date = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now= True,  null=True)
    roles = models.CharField(max_length=30, choices=ROLES, default='user', blank=True, null=True)
    


    class Meta:
        verbose_name = ("Profile")
  
   

    def __str__(self):
        return '{} Profile.'.format(self.user.username)
 
    def save(self, *args, **kwargs):
        super(User_Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.width > 300 or img.height > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_Profile.objects.create(user=instance)







