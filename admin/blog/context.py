from blog.models import blog_Category,blog_Tag
from django.utils.encoding import uri_to_iri
from django.shortcuts import  redirect, render, get_object_or_404  

def get_filters(request):



    context={
        'categories': blog_Category.objects.filter(active=True),
        'tags':blog_Tag.objects.filter(active=True),
    }
    return context

#def latest_Any(request):
    #blogs = Blog.objects.order_by('-publish_date')[:5]
    #return {'latest_Any': blogs}