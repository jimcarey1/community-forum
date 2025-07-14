from django.urls import path

from .views import create_comment, create_thread, detail_category, detail_forum, detail_thread

urlpatterns = [
    path('forum/<int:id>/create', create_thread, name='create_thread_url'),
    path('thread/<int:id>/comment', create_comment, name='create_comment_url'),
    path('category/<int:id>/', detail_category, name='detail_category_url'),
    path('forum/<int:id>/', detail_forum, name='detail_forum_url'),
    path('thread/<int:id>/', detail_thread, name='detail_thread_url'),
]