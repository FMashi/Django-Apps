from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Exists, OuterRef
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model, login, authenticate
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.encoding import uri_to_iri 
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from .forms import *
from .tokens import account_activation_token
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views import View


@csrf_exempt
def login_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = get_user_model().objects.filter(email=email).first()
        if user:
            request.session['email'] = email
            return redirect('login_password')
        else:
            message = 'لم يتم العثور على حساب بعنوان البريد الإلكتروني المقدم.'
            return render(request, 'users/login_email.html', {'message': message})
    else:
        return render(request, 'users/login_email.html')
@csrf_exempt
def login_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.session.get('email')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            message = 'رمز مرور خاطئ'
            return render(request, 'users/login_email.html', {'message': message})
    else:
        return render(request, 'users/login_password.html')



@login_required(login_url='login')
def profile(request):
    profile = get_object_or_404 (User_Profile, user=request.user)

    context = {
        'title' : 'Profile', 
        'profile':profile,
        'nbar': 'profile',
    }
    template ='users/profile.html'
    return render(request,template , context)

@login_required(login_url='login')
def edit_profile(request):
    profile = get_object_or_404 (User_Profile, user=request.user)
    
    if request.method == 'POST':
        user_form =  UserUpdateForm(request.POST, instance=request.user)
        profile_form =  ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()

            new_profile = profile_form.save()
            new_profile.user = request.user
            new_profile.save()
            profile_form.cleaned_data.get('image')
            messages.success(request, 'تم حفظ التعديلات بنجاح')
    else:
        user_form =  UserUpdateForm(instance=request.user)
        profile_form =  ProfileUpdateForm(instance=request.user.profile)

    context = {
        'title': 'Edit Profile',
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': profile,
        'nbar': 'edit_profile',
        
    }
    template = 'users/edit-profile.html'
    return render(request, template, context)




def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False

            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('home')
        else:
            #for error in list(form.errors.values()):
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'هذه الخانة مطلوبه':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(request, error) 

            

    else:
        form = UserCreationForm()

    
    context = {
        'title' : 'التسجيل',
        'form': form,
        'nbar': 'register',

    }
    template = 'users/register.html'
    return render(request, template, context)

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data['password1'])
            user.save()
            #subject = 'Activate your account'
            #message = 'Please click the following link to activate your account: '
            #message += 'http://localhost:8000/activate/{}'.format(user.activation_token)
            #send_mail(subject, message, 'admin@example.com', [user.email], fail_silently=False)
            #messages.success(request, 'An email has been sent to your email address. Please check your inbox.')
            return redirect('home')
        else:
            #for error in list(form.errors.values()):
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'هذه الخانة مطلوبه':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(request, error)
    else:
        form = UserCreationForm()
    context = {
        'title' : 'التسجيل',
        'form': form,
        'nbar': 'register',

    }
    template = 'users/user_register.html'
    return render(request, template, context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f"مرحبًا بك {username}.")
            return redirect('home')
        else:
            messages.warning(request,"خطأ في اسم المستخدم أو كلمة المرور")


    context ={
        'title' : 'تسجيل الدخول',
        'nbar': 'login',
    }
    template = 'users/login.html'
        
    return render(request, template, context)


def password_reset_request(request):

	if request.method == "POST":
		password_reset_form = CustomPasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "طلب إعادة تعيين كلمة المرور"
					email_template_name = "users/password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:

						return HttpResponse('Invalid header found.')
						
					messages.success(request, 'تم إرسال رسالة تحتوي على تعليمات إعادة تعيين كلمة المرور إلى صندوق الوارد الخاص بك.')
					return redirect ("login")
			messages.error(request, 'An invalid email has been entered.')
	password_reset_form = CustomPasswordResetForm()
        
	return render(request=request, template_name="users/password/password_reset.html", context={"password_reset_form":password_reset_form})




def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('home')
    else:
        template = 'users/logout_confirm.html'
        return render(request, template)
