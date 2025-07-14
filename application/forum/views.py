from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from django.db.models import QuerySet

from .forms import ThreadForm, CommentForm
from .models import Forum, Thread, Category, Comment, Vote

def detail_category(request:HttpRequest, id:int)->HttpResponse:
    category_obj = get_object_or_404(Category, pk=id)
    return render(request, 'forum/category/detail_category.html', {'category': category_obj})

def detail_forum(request:HttpRequest, id:int)->HttpResponse:
    forum_obj = get_object_or_404(Forum, pk=id)
    return render(request, 'forum/forum/detail_forum.html', {'forum': forum_obj})

@login_required
def create_thread(request:HttpRequest, id:int):
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
    thread_obj = get_object_or_404(Thread, pk=id)
    top_level_comments = thread_obj.comments.filter(parent__isnull=True)
    form = CommentForm()
    context = {
        'thread': thread_obj, 
        'comments':top_level_comments, 
        'form': form
    }
    if request.user.is_authenticated:
        vote = Vote.objects.filter(user=request.user, thread=thread_obj).first()
        context['user_vote'] = vote.value if vote else 0
    return render(request, 'forum/thread/detail_thread.html', context)

@login_required
def create_comment(request:HttpRequest, id:int):
    thread_obj = get_object_or_404(Thread, pk=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.thread = thread_obj
            comment.save()
            return redirect('detail_thread_url', id=thread_obj.id)
        return render(request, 'forum/thread/detail_thread.html', {'form': form})
    else:
        form = CommentForm()
        return render(request, 'forum/thread/detail_thread.html', {'form': form})

@login_required
def vote_thread(request: HttpRequest, id: int, vote_value: int):
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