from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    pass
