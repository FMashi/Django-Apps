
import os
import time
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import format_html
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import timedelta
from uuid import uuid4
from ckeditor.fields import RichTextField
from sorl.thumbnail import get_thumbnail
class PathRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

ACTIVE = (
    (True,"نشط"),
    (False,"غير نشط"),
)
STATUS_CHOICES = (
    ('draft',"مسودة"),
    ('publish',"منشور"),
)

# Create your models here.
class blog_Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank=True, allow_unicode=True, max_length=250, unique=True, null=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(default='person.png', upload_to=PathRename('images/blog/Category/'))
    active = models.BooleanField(default=True ,choices=ACTIVE)
  
    
    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'Category'

    def __str__(self):
       return self.name

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.slug, allow_unicode = True) 
        super(blog_Category, self).save(*args, **kwargs) 
        return super(blog_Category, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return 'blog/{}' .format(self.slug) 

class blog_Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='اسم الفئة')
    slug = models.SlugField(blank=True, allow_unicode=True, max_length=250, unique=True, null=True, verbose_name='الرابط')
    description = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(default='person.png', upload_to=PathRename('images/blog/Tag/'))
    active = models.BooleanField(default=True ,choices=ACTIVE, verbose_name='الحالة')
  
    
    class Meta:
        ordering = ['name']
        verbose_name = 'tag'
        verbose_name_plural = 'Tag'

    def __str__(self):
       return self.name

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.slug, allow_unicode = True) 
        super(blog_Tag, self).save(*args, **kwargs) 
        return super(blog_Tag, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return 'blog/{}' .format(self.slug) 


class blog_Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(blank=True, allow_unicode=True, max_length=250, unique=True)
    image = models.ImageField(upload_to=PathRename('images/blog/posts/{}'.format(time.strftime("%Y/%m/%d"))), null=True, blank=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='blog_posts')
    content = RichTextField(blank = True, null= True)
    post_date = models.DateTimeField(default=timezone.now)
    post_updated = models.DateTimeField(auto_now= True)
    category = models.ManyToManyField(blog_Category)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    #favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    num_posts = models.PositiveIntegerField(default=0)



    
    @property
    def image(self):
        if self.image:
            _thumbnail = get_thumbnail(self.image, '100x100', upscale=False, crop=False, quality=100)
            return format_html('<div style="display:inline-block; margin-right:10px;">'
                            '<img src="{}" width="{}" height="{}" style="border:1px solid #ddd; border-radius:3px;">'
                            '</div>'.format(_thumbnail.url, _thumbnail.width, _thumbnail.height))
        return "-"
    class Meta:
        ordering = ['-post_date']
        verbose_name = ("Post")
        verbose_name_plural = ("Blog")
    
    def __str__(self):
        return self.title 
    
    def save(self, *args, **kwargs):
        now = timezone.now()
        num_posts = blog_Post.objects.filter(author=self.author, published_at__gte=now-timedelta(hours=24)).count()
        if num_posts >= 50:
            raise ValidationError("You have reached the maximum number of posts for today.")
        else:
            self.slug = slugify(self.title, allow_unicode = True) 
            super(blog_Post, self).save(*args, **kwargs) 
            return super(blog_Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '/post_detail/{}' .format(self.slug) 
    
   