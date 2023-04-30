from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.db import transaction

# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework.views import APIView

from .models import Post, Media
from .forms import PostForm, MediaForm


# from .serializers import PostSerializer, ImageSerializer


class ListPosts(ListView):
    model = Post
    template_name = 'posts_bulletin.html'
    queryset = Post.objects.all().order_by('-create_datetime')
    context_object_name = 'bulletin_posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(self.queryset.get(pk='3'))
        # print(self.queryset.get(pk='3').load_files.all())
        # print(Image.objects.get(pk='2'))
        return context


class DetailPost(DetailView):
    model = Post
    template_name = 'bulletin_detail.html'
    context_object_name = 'bulletin_new'


class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'bulletin_add_post.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.FILES)
        if self.request.POST:
            context['media_form'] = MediaForm(self.request.POST, self.request.FILES)
        else:
            context['media_form'] = MediaForm()

        return context

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.id)
        form.instance.author = user
        context = self.get_context_data()
        media_form = context['media_form']
        files = self.request.FILES.getlist('upload_files')
        print(media_form.is_valid())

        if form.is_valid() and media_form.is_valid():
            post = form.save()
            for media in files:
                media_file = Media.objects.create(post_rel=post)
                media_file.upload_file = media
                media_file.save()
                post.load_files.add(media_file)

            post.main_image = files[0]
        return super().form_valid(form)


class UpdatePost(UpdateView):
    model = Post
    template_name = 'bulletin_edit_post.html'
    form_class = PostForm

    def get_object(self, queryset=None):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        # print(post.load_files.all())
        context['images'] = [p.upload_file for p in post.load_files.all()]

        # if self.request.POST:
        #     context['media_form'] = MediaForm(self.request.POST, self.request.FILES)
        # else:
        #     context['media_form'] = MediaForm()

        return context

    def form_valid(self, form):
        post = form.instance
        actual_post_load_files = post.load_files.all()  # Image objects
        image_list = list(actual_post_load_files)

        files = self.request.FILES

        # context = self.get_context_data()
        # media_form = context['media_form']
        #
        # files = self.request.FILES.getlist('upload_files')

        # if form.is_valid() and media_form.is_valid():
        #     post = form.save()
        #     for media in files:
        #         media_file = Media.objects.create(post_rel=post)
        #         media_file.upload_file = media
        #         media_file.save()
        #         # post.load_files.add(media_file)
        #         image_list.append(media_file)

        for k, v in files.items():
            if k == 'images':
                for image in files.getlist('images'):
                    new_image = Media.objects.create(post_rel=form.instance, upload_file=image)
                    new_image.save()
                    image_list.append(new_image)
                continue

            idx = int(k.split('-')[1])
            image_obj = image_list[idx]
            image_obj.upload_file = v
            image_obj.save()
            image_list[idx] = image_obj

        post.load_files.clear()
        post.load_files.set(image_list)
        print(post.load_files.all())
        return super().form_valid(form)
