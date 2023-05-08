import hashlib
from io import BytesIO

from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image as PILImage


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


# def make_thumbnail(main_image):
#     print(f'thumbnails {main_image.name}')
#     image = PILImage.open(main_image)
#     image.thumbnail((204, 204))
#     thumb_io = BytesIO()
#     image.save(thumb_io, image.format, quality=95)
#     thumbnail = InMemoryUploadedFile(thumb_io, None, f'{main_image.name}.jpeg', 'image/jpeg', thumb_io.tell(), None)
#     return thumbnail


class Media(models.Model):
    post_rel = models.ForeignKey('Post', on_delete=models.CASCADE)
    upload_file = models.FileField(upload_to=post_dir_path, blank=True)

    # is_main_images = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.upload_file.name} | ID: {self.post_rel.id} | {self.post_rel.title}'

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
    load_files = models.ManyToManyField(to=Media, blank=True)  # все изображения, загружаемые пользователем

    # def save(self, *args, **kwargs):
    #     print(args)
    #     print(kwargs)
    #     super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/bulletin/{self.id}'

    def __str__(self):
        return f'{self.title} | {self.create_datetime} | {self.author.username} | {self.category}'


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    is_accept = models.BooleanField(default=False, blank=True)
    is_rejected = models.BooleanField(default=False, blank=True)
    viewed = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return f'{self.user.username} | {self.post.title} | {self.create_datetime}'
