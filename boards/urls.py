from django.urls import path, include
from . import views

urlpatterns = [
   # path('home/', views.home, name='home'),
    path('home/', views.BoardListView.as_view(), name='home'),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('boards/<int:pk>/', views.board_topics, name='board_topics'),
    path('boards/<int:pk>/new/', views.new_topic, name='new_topic'),
    path('boards/<int:pk>/topics/<int:topic_pk>/', views.topic_posts, name='topic_posts'),
    path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
    path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
]

