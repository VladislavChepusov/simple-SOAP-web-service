from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Article)
admin.site.register(CustomUser,UserAdmin)