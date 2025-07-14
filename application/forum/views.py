from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from django.db.models import QuerySet

from .forms import ThreadForm, CommentForm
from .models import Forum, Thread, Category

def detail_category(request:HttpRequest, id:int)->HttpResponse:
    category_obj = get_object_or_404(Category, pk=id)
    return render(request, 'forum/category/detail_category.html', {'category': category_obj})

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
    return render(
        request, 
        'forum/thread/detail_thread.html', 
        {'thread': thread_obj, 'comments':top_level_comments, 'form': form})

def detail_forum(request:HttpRequest, id:int):
    forum_obj = get_object_or_404(Forum, pk=id)
    return render(request, 'forum/forum/detail_forum.html', {'forum': forum_obj})