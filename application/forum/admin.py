from django.contrib import admin

from .models import Category, Forum, Thread, Comment

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent__name']
    date_hierarchy = 'created_on'
admin.site.register(Category, CategoryAdmin)

class ForumAdmin(admin.ModelAdmin):
    list_display = ['name']
    date_hierarchy = 'created_on'
admin.site.register(Forum, ForumAdmin)

class ThreadAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'author__username', 'is_locked']
    date_hierarchy = 'created_on'
admin.site.register(Thread, ThreadAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['content', 'thread__title', 'author__username']
    date_hierarchy = 'created_on'
admin.site.register(Comment, CommentAdmin)