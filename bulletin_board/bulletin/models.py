from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


def post_dir_path(instance, filename):
    post = Post.objects.get(pk=instance.post_rel.id)
    return f'post_{post.id}/{filename}'


class Image(models.Model):
    post_rel = models.ForeignKey('Post', on_delete=models.CASCADE)
    file = models.FileField(upload_to=post_dir_path)
    is_main_images = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.file.name} | ID: {self.post_rel.id} | {self.post_rel.title}'


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    create_datetime = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    load_files = models.ManyToManyField(to=Image, blank=True)

    def __str__(self):
        return f'{self.title} | {self.create_datetime} | {self.author.username} | {self.category}'

    def path_to_main_image(self):
        # return 'Эээй'
        # print(self.load_files.all())
        # print(self.load_files.all().filter(is_main_images=True))
        return self.load_files.all().filter(is_main_images=True)[0].file
        # return self.load_files.get(is_main_images=True).file


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    create_datatime = models.DateTimeField(auto_now_add=True)
    is_accept = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} | {self.post.title} | {self.create_datatime}'
