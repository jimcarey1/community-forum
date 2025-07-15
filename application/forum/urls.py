from django.urls import path, register_converter

from utils.converters import NegativeIntConverter

from .views import create_comment, create_thread, detail_category, detail_forum, detail_thread, vote_thread, vote_comment

register_converter(NegativeIntConverter, 'negint')

urlpatterns = [
    path('forum/<int:id>/create', create_thread, name='create_thread_url'),
    path('thread/<int:id>/comment', create_comment, name='create_comment_url'),
    path('category/<int:id>/', detail_category, name='detail_category_url'),
    path('forum/<int:id>/', detail_forum, name='detail_forum_url'),
    path('thread/<int:id>/', detail_thread, name='detail_thread_url'),
    path('thread/<int:id>/vote/<negint:vote_value>', vote_thread, name='vote_thread_url'),
    path('comment/<int:id>/vote/<negint:vote_value>', vote_comment, name='vote_comment_url'),
]