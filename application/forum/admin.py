from django.contrib import admin

from .models import Category, Forum, Thread, Comment

class CategoryAdmin(admin.ModelAdmin):
    """
    Admin options for the Category model.
    Displays name and parent name, and allows filtering by creation date.
    """
    list_display = ['name', 'parent__name']
    date_hierarchy = 'created_on'
admin.site.register(Category, CategoryAdmin)

class ForumAdmin(admin.ModelAdmin):
    """
    Admin options for the Forum model.
    Displays name and allows filtering by creation date.
    """
    list_display = ['name']
    date_hierarchy = 'created_on'
admin.site.register(Forum, ForumAdmin)

class ThreadAdmin(admin.ModelAdmin):
    """
    Admin options for the Thread model.
    Displays title, content, author username, and lock status, and allows filtering by creation date.
    """
    list_display = ['title', 'content', 'author__username', 'is_locked']
    date_hierarchy = 'created_on'
admin.site.register(Thread, ThreadAdmin)

class CommentAdmin(admin.ModelAdmin):
    """
    Admin options for the Comment model.
    Displays content, associated thread title, and author username, and allows filtering by creation date.
    """
    list_display = ['content', 'thread__title', 'author__username']
    date_hierarchy = 'created_on'
admin.site.register(Comment, CommentAdmin)