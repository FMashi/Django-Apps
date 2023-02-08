from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
# Create your views here.
User = get_user_model()

@user_passes_test(lambda u: u.is_superuser)
def home(request):


    context = {

    }
    return render(request, 'index.html', context)



def error_403(request, exception):
   context = {
    'title': 'ليس لديك صلاحية وصول',
   }
   return render(request, 'error/403.html', context)

def error_400(request, exception):
   context = {
    'title': 'اقتراح غير جيد',
   }
   return render(request, 'error/400.html', context)


def error_404(request, exception):
   context = {
    'title': 'الصفحه غير موجودة',


   }
   return render(request, 'error/404.html', context)

def error_500(request):
   context = {
    'title': 'خطأ خادم داخلي',
   }
   return render(request, 'error/500.html', context)

