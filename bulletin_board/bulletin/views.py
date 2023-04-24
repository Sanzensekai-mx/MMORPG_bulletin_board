from django.shortcuts import render

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Image
from .forms import PostForm
from .serializers import PostSerializer, ImageSerializer


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
        # form.save()
        # main_image = form.instance.load_files.all().first()
        # form.instance.main_image = main_image.upload_image
        return super().form_valid(form)


class PostUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        print(1)
        # images = request.FILES.getlist('image')
        images = request.FILES # !!!!!!!!
        image_serializer = ImageSerializer(data={'image': images}, many=True)
        if image_serializer.is_valid():
            print(image_serializer)
        print(request.POST)
        print(request.FILES)  # !!!
        # {'images-0': [<InMemoryUploadedFile: 36f48fee328e065a4e89c4272f16e767--batman-christian-bale-christian-grey.jpg (image/jpeg)>]}>
        # print(request.FILES.getlist('image'))
        return Response()
