from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


from forum.models import Category, Forum

def index(request:HttpRequest)->HttpResponse:
    categories = Category.objects.prefetch_related('forums')
    return render(request, 'core/index.html', {'categories': categories})