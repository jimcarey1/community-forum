"""
This module defines the views for the forum application.
It handles requests related to categories, forums, threads, comments, and voting.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from django.db.models import QuerySet
from django.forms import Form

from .forms import ThreadForm, CommentForm
from .models import Forum, Thread, Category, Comment, Vote, CommentVote

@login_required
def vote_comment(request: HttpRequest, id: int, vote_value: int):
    """
    Handles voting on comments. Allows users to upvote, downvote, or remove their vote.
    Returns a JSON response with the total votes for the comment and the user's current vote.
    """
    comment = get_object_or_404(Comment, pk=id)
    vote, created = CommentVote.objects.get_or_create(
        user=request.user,
        comment=comment,
        defaults={'value': vote_value}
    )
    
    new_vote_value = vote_value

    if not created:
        if vote.value == vote_value:
            vote.delete()
            new_vote_value = 0 # Vote removed
        else:
            vote.value = vote_value
            vote.save()
            new_vote_value = vote_value

    return JsonResponse({'total_votes': comment.total_votes, 'user_vote': new_vote_value})


def detail_category(request:HttpRequest, id:int)->HttpResponse:
    """
    Displays the details of a specific category, including its forums.
    """
    category_obj = get_object_or_404(Category, pk=id)
    return render(request, 'forum/category/detail_category.html', {'category': category_obj})

def detail_forum(request:HttpRequest, id:int)->HttpResponse:
    """
    Displays the details of a specific forum, including its threads.
    """
    forum_obj = get_object_or_404(Forum, pk=id)
    return render(request, 'forum/forum/detail_forum.html', {'forum': forum_obj})

@login_required
def create_thread(request:HttpRequest, id:int):
    """
    Handles the creation of a new thread within a specified forum.
    Requires user to be logged in.
    """
    forum_obj = get_object_or_404(Forum, pk=id)
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.forum = forum_obj
            thread.save()
            return redirect('detail_thread_url', id=thread.id)
        return render(request, 'forum/thread/new_thread.html', {'form':form})
    else:
        form = ThreadForm()
        return render(request, 'forum/thread/new_thread.html', {'form': form})
    
def detail_thread(request:HttpRequest, id:int):
    """
    Displays the details of a specific thread, including its comments.
    Also handles displaying user's vote on the thread and comments if logged in.
    """
    thread_obj = get_object_or_404(Thread, pk=id)
    top_level_comments = thread_obj.comments.filter(parent__isnull=True)
    form:Form = CommentForm()
    context = {
        'thread': thread_obj, 
        'comments':top_level_comments, 
        'form': form
    }
    if request.user.is_authenticated:
        vote = Vote.objects.filter(user=request.user, thread=thread_obj).first()
        context['user_vote'] = vote.value if vote else 0
        
        def set_comment_user_vote_and_form(comments_qs):
            for comment in comments_qs:
                comment_vote = CommentVote.objects.filter(user=request.user, comment=comment).first()
                comment.user_vote = comment_vote.value if comment_vote else 0
                comment.reply_form = CommentForm(prefix=f'comment_{comment.id}')
                if comment.child_comments.exists():
                    set_comment_user_vote_and_form(comment.child_comments.all())
        
        set_comment_user_vote_and_form(top_level_comments)
    print(form.fields['content'].widget, form.fields['content'].__dict__)

    return render(request, 'forum/thread/detail_thread.html', context)

@login_required
def create_comment(request:HttpRequest, id:int):
    """
    Handles the creation of a new comment on a specified thread.
    Requires user to be logged in.
    """
    thread_obj = get_object_or_404(Thread, pk=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            print('The form is valid.')
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = thread_obj
            parent_id = request.POST.get('parent')
            if parent_id:
                comment.parent = get_object_or_404(Comment, pk=parent_id)
            comment.save()
            return redirect('detail_thread_url', id=thread_obj.id)
        return render(request, 'forum/thread/detail_thread.html', {'form': form, 'thread': thread_obj})
    else:
        form = CommentForm()
        return render(request, 'forum/thread/detail_thread.html', {'form': form, 'thread': thread_obj})

@login_required
def vote_thread(request: HttpRequest, id: int, vote_value: int):
    """
    Handles voting on threads. Allows users to upvote, downvote, or remove their vote.
    Returns a JSON response with the total votes for the thread and the user's current vote.
    """
    thread = get_object_or_404(Thread, pk=id)
    vote, created = Vote.objects.get_or_create(
        user=request.user,
        thread=thread,
        defaults={'value': vote_value}
    )
    
    new_vote_value = vote_value

    if not created:
        if vote.value == vote_value:
            vote.delete()
            new_vote_value = 0 # Vote removed
        else:
            vote.value = vote_value
            vote.save()
            new_vote_value = vote_value

    return JsonResponse({'total_votes': thread.total_votes, 'user_vote': new_vote_value})