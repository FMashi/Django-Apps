from django.contrib import admin
from .models import User, User_Profile

#admin.site.unregister(User)
admin.site.register(User_Profile)
