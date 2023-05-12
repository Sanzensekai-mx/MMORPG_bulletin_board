import json
from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse

from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, Media, Reply
from .forms import PostForm, MediaForm, ReplyTextArea
from .serializers import AcceptReplyStatusSerializer, RejectReplyStatusSerializer
from .signals import update_reply_signal


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


class DetailPost(DetailView, FormMixin):
    model = Post
    template_name = 'bulletin_detail.html'
    context_object_name = 'bulletin_new'
    form_class = ReplyTextArea

    def get_success_url(self):
        return reverse('bulletin_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        # post = Post.objects.get(pk=kwargs['object'].id)
        post = self.object
        all_media = post.load_files.all()
        context['reply_send'] = ReplyTextArea()
        if all_media:
            context['first_media'] = all_media[0]
            context['rest_of_media'] = all_media[1:]

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        user = request.user
        is_reply_exist = Reply.objects.filter(user=user, post=self.object).exists()

        if form.is_valid() and not is_reply_exist:
            reply = form.save(commit=False)
            reply.post = self.object
            reply.user = user
            reply.save()

            return self.form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form,
                                                                 error_message='Вы уже отправили отклик на объявление'))
            # return self.form_invalid(form)


class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'bulletin_add_post.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        form = PostForm()
        media_form = MediaForm()
        return render(request, self.template_name, {'form': form, 'media_form': media_form})

    def post(self, request, *args, **kwargs):
        # self.object = self.get_object()
        user = User.objects.get(pk=request.user.id)
        # context = self.get_context_data()
        post_form = PostForm(request.POST)
        media_form = MediaForm(request.POST, request.FILES)
        files = request.FILES.getlist('upload_files')

        post_form.instance.author = user

        if post_form.is_valid() and media_form.is_valid():
            post = post_form.save()
            for media in files:
                media_file = Media.objects.create(post_rel=post)
                media_file.upload_file = media
                media_file.save()
                post.load_files.add(media_file)

            post.main_image = files[0]
            return self.form_valid(post_form)
        else:
            return render(request, self.template_name, {'form': post_form, 'media_form': media_form})


class UpdatePost(LoginRequiredMixin, UpdateView):
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

        return context

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        post_media = post.load_files.all()
        deleted_images = request.POST.get('deleted_images', '[]')
        deleted_images = json.loads(deleted_images)

        files = request.FILES.getlist('images')
        for media_idx in deleted_images:
            media = post_media[media_idx]
            media.delete()
            # print(post_media[media_idx])

        for media in files:
            new_media = Media.objects.create(post_rel=post, upload_file=media)
            new_media.save()
            post.load_files.add(new_media)

        return super().post(request, *args, **kwargs)


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'bulletin_delete.html'
    context_object_name = 'post_to_del'
    success_url = '/'


class UserSelfPostsReplies(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'user_reply_private_page.html'

    def get_queryset(self):
        queryset = Reply.objects.filter(post__author=self.request.user).order_by('-create_datetime')
        if self.request.GET.get('post_id'):
            post_id = self.request.GET.get('post_id')
            queryset = Reply.objects.filter(post__pk=post_id).order_by('-create_datetime')
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['queryset'] = self.get_queryset()
        user_posts = Post.objects.filter(author=self.request.user)
        # context['user_posts'] = Post.objects.filter(author=self.request.user)
        filter_post_pagination = Paginator(user_posts, 10)
        context['posts_paginator'] = filter_post_pagination
        context['page_obj'] = filter_post_pagination.page(self.request.GET.get('page', 1))
        if self.request.GET.get('post_id'):
            post_id = self.request.GET.get('post_id')
            print(Post.objects.get(pk=post_id))
            context['current_post'] = Post.objects.get(pk=post_id)
        else:
            context['current_post'] = None
        return context


class AcceptReplyStatusAPIView(APIView):
    def post(self, request, pk):
        reply = Reply.objects.get(pk=pk)
        if reply.is_accept is False and reply.is_rejected is False:
            reply.is_accept = True
            reply.viewed = True
            reply.save()
            print(request.data)
            update_reply_signal.send(sender=Reply, instance=reply, is_accept=True)
            return Response({'success': True})
        else:
            return Response({'success': False})


class RejectReplyStatusAPIView(APIView):
    def post(self, request, pk):
        reply = Reply.objects.get(pk=pk)
        if reply.is_accept is False and reply.is_rejected is False:
            reply.is_rejected = True
            reply.viewed = True
            reply.save()
            print(request.data)
            update_reply_signal.send(sender=Reply, instance=reply, is_accept=False)
            return Response({'success': True})
        else:
            return Response({'success': False})
