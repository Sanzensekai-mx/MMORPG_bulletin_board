from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Posts


class ListPosts(ListView):
    model = Posts
    template_name = 'posts_bulletin.html'
    queryset = Posts.objects.all().order_by('-create_datetime')
    context_object_name = 'bulletin_posts'


