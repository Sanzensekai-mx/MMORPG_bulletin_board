from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from rest_framework.views import APIView

from .models import Post, Image
from .forms import PostForm


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

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.id)
        form.instance.author = user
        post = form.save(commit=False)
        post.save()

        files = self.request.FILES.getlist('images')
        print(self.request.FILES)
        print(files)

        images_obj = []
        for file in files:
            image_obj = Image.objects.create(post_rel=post, upload_image=file)
            image_obj.save()
            images_obj.append(image_obj)

        post.main_image = files[0]
        post.load_files.set(images_obj)
        post.save()

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
        context['images'] = [p.upload_image for p in post.load_files.all()]
        return context

    def form_valid(self, form):
        post = form.instance
        actual_post_load_files = post.load_files.all()  # Image objects
        image_list = list(actual_post_load_files)
        # print(image_list)
        files = self.request.FILES  # files from request
        print(files)

        for k, v in files.items():
            if k == 'images':
                for image in files.getlist('images'):
                    new_image = Image.objects.create(post_rel=form.instance, upload_image=image)
                    new_image.save()
                    image_list.append(new_image)
                continue

            idx = int(k.split('-')[1])
            image_obj = image_list[idx]
            image_obj.upload_image = v
            image_obj.save()
            image_list[idx] = image_obj

        post.load_files.clear()
        post.load_files.set(image_list)
        print(post.load_files.all())
        return super().form_valid(form)

# class PostUploadView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#
#     def post(self, request, *args, **kwargs):
#         # images = request.FILES.getlist('image')
#         print(request.FILES)  # !!!
#
#         images = request.FILES.getlist('images')  # !!!!!!!!
#         print(images)
#         image_serializer = ImageSerializer(data={'image': images}, many=True)
#         if image_serializer.is_valid():
#             print(1)
#             print(image_serializer)
#         print(request.POST)
#         print(Post.objects.filter(title=request.POST['title'][0]))
#
#         # {'images-0': [<InMemoryUploadedFile: 36f48fee328e065a4e89c4272f16e767--batman-christian-bale-christian-grey.jpg (image/jpeg)>]}>
#         # print(request.FILES.getlist('image'))
#         return Response()
