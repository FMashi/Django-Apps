from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import PasswordResetForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django_countries.widgets import CountrySelectWidget
from datetime import datetime
import datetime
from django.utils.translation import gettext_lazy as _
#from django_countries import countries

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Enter Email AdDress'}))


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='كلمة المرور',
        widget=forms.PasswordInput(attrs ={ 'class': 'form-control form-control-user','placeholder': 'أدخل كلمة المرور الخاصة بك'}),
        min_length=8,
        #help_text= 'يجب أن تكون على الاقل 8 رموز ',
        )
    password2 = forms.CharField(label='تاكيد كلمة المرور',
        widget=forms.PasswordInput(attrs ={ 'class': 'form-control form-control-user','placeholder': 'أدخل تاكيد كلمة المرور'}),
        min_length=8,
        )
    check = forms.BooleanField(required = True,
        label="",
        help_text= 'أنت توافق على شروط الخدمة في الموقع وتُقرّ بقراءة سياسة الخصوصية ',
        )
    
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')
        labels={
           
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'password1' : 'كلمة المرور',
            'password2': 'تاكيد كلمة المرور',
        }
     
        widgets = {
            'username': forms.TextInput(attrs ={ 'class': 'form-control form-control-user','placeholder': 'أدخل اسم المستخدم الخاص بالحساب'}),
            'first_name' : forms.TextInput(attrs ={ 'class': 'form-control form-control-user','placeholder': 'أكتب اسمك'}),
            'last_name' : forms.TextInput(attrs ={ 'class': 'form-control form-control-user','placeholder': 'أكتب اسم العائلة '}),
            'email': forms.TextInput(attrs ={ 'class': 'form-control form-control-user','placeholder': 'أدخل البريد الإلكتروني الخاص بك'}),
            'password1' : forms.PasswordInput(attrs ={ 'class': 'form-control form-control-user','placeholder': 'أدخل كلمة المرور الخاصة بك'}),
            'password2': forms.PasswordInput(attrs ={ 'class': 'form-control form-control-user','placeholder': 'أدخل تاكيد كلمة المرور'}),
            }
        error_messages = {
            #"first_name": {"required": _("name field is required."),},
            #"password1": {"required": _("password field is required."),},
        }
        help_texts={
            'username':'اسم المستخدم يجب أن لا يحتوي على مسافات',
        }
        captcha = ReCaptchaField(label='أنت لست انسان الي؟',
        widget=ReCaptchaV2Checkbox,
        )


    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd ['password2']:
            raise forms.ValidationError('كلمة المرور غير متطابقة')
        return cd['password2']    


    def clean_username(self):
        cd = self.cleaned_data  
        if User.objects.filter(username=cd['username']).exists():
            raise forms.ValidationError('اسم المستخدم غير متاح')
        return cd['username']   

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username' ,'first_name', 'last_name', 'email')
        labels={
           
            'username': 'اسم المستخدم',
            'first_name': 'الإسم',
            'last_name' : 'اسم العائلة',
            'email': 'البريد الإلكتروني',
        }
     
        widgets = {
            'username': forms.TextInput(attrs ={ 'class': 'form-control','placeholder': 'أدخل اسم المستخدم الخاص بالحساب'}),
            'first_name' : forms.TextInput(attrs ={ 'class': 'form-control','placeholder': 'أكتب اسمك'}),
            'last_name' : forms.TextInput(attrs ={ 'class': 'form-control','placeholder': 'أكتب اسم العائلة '}),
            'email': forms.TextInput(attrs ={ 'class': 'form-control','placeholder': 'أدخل البريد الإلكتروني الخاص بك'}),
            }
        help_texts={
            'username': ' اسم المستخدم يجب ألا يحتوي على مسافات',
        }

        

        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User_Profile
        fields = ('image','bio',)
        labels={
            'bio': 'النبذة التعريفية',
        }
     
        widgets = {
            'bio': forms.TextInput(attrs ={ 'class': 'form-control form-control-user','placeholder': 'أضف نبذة تعريفية لملفك الشخصي'}),
            }
       

class LoginForm(forms.ModelForm):
    class Meta:
        username = forms.CharField(
        label='اسم المستخدم',
        widget= forms.TextInput(attrs ={ 'class': 'form-control form-control-user'}),
        )
        password = forms.CharField(
        label='كلمة المرور',
        widget= forms.PasswordInput(attrs ={ 'class': 'form-control form-control-user'}),
        )

        model = User
        fields = ('username', 'password',)
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    
        


