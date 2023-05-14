import json
from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse

from django.core.paginator import Paginator

from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMultiAlternatives

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, Media, Reply
from .forms import PostForm, MediaForm, ReplyTextArea, SendNewsMails

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
        context['images_ext'] = ['jpg', 'jpeg', 'png']
        context['video_ext'] = ['mp4']
        if list(all_media):
            context['first_media'] = all_media[0]
            context['first_media_ext'] = all_media[0].upload_file.name.split('.')[-1]
            context['rest_of_media'] = all_media[1:]
            context['rest_of_media_ext'] = [i.upload_file.name.split('.')[-1] for i in all_media[1:]]

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
            if len(files) > 0:
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
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        # print(post.load_files.all())
        context['images'] = [p.upload_file for p in post.load_files.all()]
        context['media_form'] = MediaForm()

        return context

    def post(self, request, *args, **kwargs):
        # post_form = self.get_form()
        # post_form.instance.author = request.user
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        post_media = post.load_files.all()
        deleted_images = request.POST.get('deleted_images', '[]')
        files = request.FILES.getlist('upload_files')
        media_form = MediaForm(request.POST, request.FILES)

        post_media = list(post_media)  # !!! обязательно в преобразовать qs в список

        print(len(post_media))

        if deleted_images:
            # post_media = list(post_media)  # !!! обязательно в преобразовать qs в список
            if post_media:
                deleted_images = json.loads(deleted_images)
                for media_idx in deleted_images:
                    post_media[media_idx] = None
                post_media = [i for i in post_media if i]

        if media_form.is_valid():
            # if files:
            for media in files:
                new_media = Media.objects.create(post_rel=post, upload_file=media)
                new_media.save()
                post_media.append(new_media)

            post.main_image = post_media[0]
            post.load_files.clear()
            post.load_files.set(post_media)
            return super().post(request, *args, **kwargs)
        else:
            context_data = self.get_context_data()
            context_data['media_form'] = media_form
            return render(request, self.template_name,
                          context=context_data)

    def form_valid(self, form):
        post = form.instance
        files = list(post.load_files.all())
        if len(files) > 0:
            post.main_image = files[0].upload_file
        else:
            post.main_image = None

        return super().form_valid(form)


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
            context['current_post'] = Post.objects.get(id=post_id)
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


@staff_member_required
def admin_send_news_mail_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        content = request.POST.get('content')

        users = User.objects.all()

        for user in users:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=content,
                to=[user.email]
            )

            msg.send()

        return render(request, 'success_notify.html')

    admin_form = SendNewsMails()
    return render(request, 'admin_news_notify.html', context={'admin_form': admin_form})
