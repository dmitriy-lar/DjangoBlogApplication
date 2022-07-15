from django.urls import path
from .views import index, category, search, post, profile, update, my_posts, create_post, update_post, delete_post
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', index, name='index'),
    path('category/<int:pk>/', category, name='category'),
    path('search_result/', search, name='search'),
    path('post/<str:pk>/', post, name='post'),
    path('profile', profile, name='profile'),
    path('update/', update, name='update'),
    path('my-posts/', my_posts, name='my_posts'),
    path('create-post/', create_post, name='create_post'),
    path('update-post/<str:pk>/', update_post, name='update_post'),
    path('delete-post/<str:pk>/', delete_post, name='delete_post')


]