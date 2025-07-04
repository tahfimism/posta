from django.contrib import admin

# Register your models here.
from .models import User, Post

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp', 'like_count')
    search_fields = ('user__username', 'content')
    list_filter = ('timestamp', 'user')
    ordering = ('-timestamp',)

