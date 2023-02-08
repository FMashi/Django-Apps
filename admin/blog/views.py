from django.shortcuts import render
from .models import *
from blog.forms import *
from django.shortcuts import  redirect, render, get_object_or_404 
from django.utils.encoding import uri_to_iri 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def post_list(request):
    posts = blog_Post.objects.filter(status='publish')
    
    paginator = Paginator(posts,9)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_page)    

    context = {
        'title': 'blog',
        'nbar': 'blog',
        'posts': posts,
        'page': page,

        'category': blog_Category.objects.filter(active=True),
    }
    templates= 'blog/post_list.html'
    return render(request, templates,  context)

def post_detail(request, slug):
    post=get_object_or_404 (blog_Post, slug=uri_to_iri(slug))

    #is_fav = False
    #if post.favourites.filter(id=request.user.id).exists():
        #is_fav = True

    context = {
        'title': post,
        'post': post,
        #'is_fav':is_fav,    
    }
    templates= 'blog/post_detail.html'
    return render(request, templates, context)

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    templates= 'blog/post_form.html'
    return render(request, templates,context)

def post_update(request, pk):
    post = get_object_or_404(blog_Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
    }
    templates= 'blog/post_form.html'
    return render(request, templates, context)

def post_remove(request, pk):
    post = get_object_or_404(blog_Post, pk=pk)
    post.delete()
    return redirect('post_list')



def blog_category_list(request):
    categories = blog_Category.objects.filter(active=True)
    context = {
        'title': 'categories',
        'categories': categories,
        }

    templates= 'blog/category_list.html'
    return render(request, templates,  context)

def blog_category_detail(request, slug):
    category=get_object_or_404 (blog_Category, slug=uri_to_iri(slug))

    context = {
        'title': category.name,
        'category': category,  
    }
    templates= 'blog/category_detail.html'
    return render(request, templates, context)

def blog_category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm()

    context = {
        'form': form,
    }
    templates= 'blog/category_form.html'
    return render(request, templates,context)

def blog_category_update(request, pk):
    category = get_object_or_404(blog_Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            category = form.save()
            return redirect('post_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)

    context = {
        'form': form,
    }
    templates= 'blog/category_form.html'
    return render(request, templates, context)


def blog_category_remove(request, pk):
    category = get_object_or_404(blog_Category, pk=pk)
    category.delete()
    return redirect('category_list')







