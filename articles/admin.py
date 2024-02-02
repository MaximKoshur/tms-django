from django.contrib import admin
from .models import Article, Author
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'date_of_birth', ),
        }),
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'like_count', 'is_popular')
    search_fields = ('name', 'text')
    readonly_fields = ('like_count', 'is_popular')
    fieldsets = (
        ('Default', {
            'fields': ('name', 'like_count', 'author', 'is_popular'),
        }),
        ('Content', {
            'fields': ('text',),
        }),
    )

