from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import blog_Post,blog_Category,blog_Tag

class PostForm(forms.ModelForm):
    #content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = blog_Post
        exclude = ['author']
        fields = ['title', 'image', 'author', 'content', 'post_date', 'category', 'status']
        help_texts = {
        'title': 'Please enter a title for the post',
        'content': 'Please enter the content of the post',
        }
        labels = {
            'title': 'Post Title',
            'image': 'Post Image',
            'author': 'Author',
            'content': 'Post Content',
            'post_date': 'Post Date',
            'category': 'Post Category',
            'status': 'Post Status',
        }


        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.CharField(widget=CKEditorWidget(attrs={'class': 'form-control'})),
            'post_date': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'status': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
        error_messages = {
    'title': {
        'unique': 'A post with the same title already exists.',
        'max_length': 'Title should not exceed 200 characters.',
    },
    'content': {
        'required': 'Content is required for a post.',
        'max_length': 'Content should not exceed 10000 characters.',
    },
    'image': {
        'invalid': 'Please upload a valid image.',
        'required': 'Image is required for a post.'
    },
    'post_date': {
        'required': 'Post date is required for a post.'
    },
    'post_updated': {
        'required': 'Post update is required for a post.'
    },
    'category': {
        'required': 'Please select at least one category for the post.'
    },
    'status': {
        'required': 'Please select a status for the post.'
    },
}




class CategoryForm(forms.ModelForm):
    class Meta:
        model = blog_Category
        fields = ['name', 'slug','image','description','active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'active' : forms.Select(attrs ={ 'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'slug': 'Slug',
            'image': 'Image',
            'description': 'Description',
            'active':'active',
        }
        help_texts = {
            'slug': 'A slug is a short label that identifies the category. It is used as part of the URL.',
        }
        error_messages = {
            'title': {
                'required': 'Please enter a title for the category.',
            },
            'slug': {
                'required': 'Please enter a slug for the category.',
                'unique': 'A category with the same slug already exists.',
            },
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = blog_Tag
        fields = ['name', 'slug','image','description','active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'active' : forms.Select(attrs ={ 'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'slug': 'Slug',
            'image': 'Image',
            'description': 'Description',
            'active':'active',
        }
        help_texts = {
            'slug': 'A slug is a short label that identifies the category. It is used as part of the URL.',
        }
        error_messages = {
            'title': {
                'required': 'Please enter a title for the category.',
            },
            'slug': {
                'required': 'Please enter a slug for the category.',
                'unique': 'A category with the same slug already exists.',
            },
        }
