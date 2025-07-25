"""
This module defines the database models for the forum application.
It includes models for categories, forums, threads, comments, and votes.
"""
from django.db import models
from django.db.models import Sum

from django_ckeditor_5.fields import CKEditor5Field

from users.models import User
from utils.slug_field import slug_field

# Create your models here.
class Category(models.Model):
    """
    Represents a category in the forum. Categories can have a parent, forming a hierarchical structure.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=40, blank=True)
    description = models.TextField(default='This category does not have any description.')
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        Returns the string representation of the category, which is its name.
        """
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a slug if it's not provided.
        """
        if not self.slug:
            self.slug = slug_field(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'categories'
    
    @classmethod
    def root(cls):
        """
        Returns all root categories (categories with no parent).
        """
        return cls._default_manager.filter(parent=None)

class Forum(models.Model):
    """
    Represents a forum within a category. Forums contain threads.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=40, blank=True)
    description = models.TextField(default='This category does not have any descripiton.')
    category = models.ForeignKey('Category', related_name='forums', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        Returns the string representation of the forum, which is its name.
        """
        return self.name
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a slug if it's not provided.
        """
        if not self.slug:
            self.slug = slug_field(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'forums'

class Thread(models.Model):
    """
    Represents a thread within a forum. Threads are created by users and contain comments.
    """
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=40, blank=True)
    content = CKEditor5Field('Content', config_name='extends')
    author = models.ForeignKey(User, related_name='threads', on_delete=models.DO_NOTHING)
    forum = models.ForeignKey(Forum, related_name='threads', on_delete=models.CASCADE)
    is_locked = models.BooleanField(default=False, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        Returns the string representation of the thread, which is its title.
        """
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate a slug if it's not provided.
        """
        if not self.slug:
            self.slug = slug_field(self.title)
        super().save(*args, **kwargs)
    
    @property
    def total_votes(self):
        """
        Calculates the total number of votes for the thread.
        """
        return self.votes.aggregate(total=Sum('value'))['total'] or 0
    
    class Meta:
        db_table = 'threads'
        ordering = ['-created_on']
        permissions = [('can_lock', 'Can Lock')]

class Vote(models.Model):
    """
    Represents a user's vote on a thread.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name='votes', on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        db_table = 'thread_votes'
        unique_together = ('user', 'thread')
    
class Comment(models.Model):
    """
    Represents a comment on a thread. Comments can be nested (have a parent comment).
    """
    content = CKEditor5Field('Content', config_name='extends')
    parent = models.ForeignKey('self', related_name='child_comments', on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.DO_NOTHING)
    thread = models.ForeignKey(Thread, related_name='comments', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        """
        Returns a truncated string representation of the comment content.
        """
        return self.content[:50]
    
    @property
    def total_votes(self):
        """
        Calculates the total number of votes for the comment.
        """
        return self.votes.aggregate(total=Sum('value'))['total'] or 0
    
    class Meta:
        db_table = 'comments'

class CommentVote(models.Model):
    """
    Represents a user's vote on a comment.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='votes', on_delete=models.CASCADE)
    value = models.IntegerField()

    class Meta:
        db_table = 'comment_votes'
        unique_together = ('user', 'comment')
