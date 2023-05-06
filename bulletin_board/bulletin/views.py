import json
from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse

from .models import Post, Media
from .forms import PostForm, MediaForm, ReplyTextArea


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

        post = Post.objects.get(pk=kwargs['object'].id)
        all_media = post.load_files.all()
        context['reply_send'] = ReplyTextArea()
        if all_media:
            context['first_media'] = all_media[0]
            context['rest_of_media'] = all_media[1:]

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = self.object
            reply.user = request.user
            reply.save()

            return self.form_valid(form)

        else:
            return self.form_invalid(form)


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


class DeletePost(DeleteView):
    model = Post
    template_name = 'bulletin_delete.html'
    context_object_name = 'post_to_del'
    success_url = '/'
