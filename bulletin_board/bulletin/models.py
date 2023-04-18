import hashlib

from django.db import models
from django.contrib.auth.models import User

from PIL import Image


# from mixins import ResizeImageMixin

class MoreThanOneMainImage(Exception):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def post_dir_path(instance, filename):
    post = Post.objects.get(pk=instance.post_rel.id)
    return f'post_{post.id}/{filename}'


def main_image_post_dir_path(instance, filename):
    # post = Post.objects.get(pk=instance.post_rel.id)
    return f'post_{instance.id}/main_{filename}'


class Image(models.Model):
    post_rel = models.ForeignKey('Post', on_delete=models.CASCADE)
    upload_image = models.ImageField(upload_to=post_dir_path)

    # is_main_images = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.upload_image.name} | ID: {self.post_rel.id} | {self.post_rel.title}'

    # def save(self, **kwargs):
    #     if len(Image.objects.filter(post_rel=self.post_rel, is_main_images=True)) > 1:
    #         raise MoreThanOneMainImage
    #     super().save(self, kwargs)
    #
    #     SIZE = 236, 177
    #     # print(self.instance.file)
    #     print(self.file)
    #     # сохранение изображение нужного размера для карточки
    # if self.is_main_images:
    #     print(self.instance.file)


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    main_image = models.ImageField(upload_to=main_image_post_dir_path, blank=True)  # фиксированный размер должен быть
    load_files = models.ManyToManyField(to=Image, blank=True)  # все изображения, загружаемые пользователем

    def __str__(self):
        return f'{self.title} | {self.create_datetime} | {self.author.username} | {self.category}'

    # def path_to_main_image(self):
    #     return self.load_files.all().filter(is_main_images=True)[0].file


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    create_datatime = models.DateTimeField(auto_now_add=True)
    is_accept = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} | {self.post.title} | {self.create_datatime}'
