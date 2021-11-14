from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'date_joined',)
    ordering = ('-date_joined', 'username',)
    search_fields = ('username',)
    readonly_fields = ('id', )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at',)
    ordering = ('-created_at', 'id',)
    search_fields = ('id',)
    readonly_fields = ('id', 'created_at', )
