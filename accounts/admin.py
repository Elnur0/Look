from django.contrib.auth import get_user_model
from django.contrib import admin

# Register your models here.

from .models import MyUser, Profile


User = get_user_model()

admin.site.register(User)
admin.site.register(Profile)