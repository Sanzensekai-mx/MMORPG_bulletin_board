from django.contrib import admin
from .models import *
from django import forms


class FileInline(admin.TabularInline):
    model = Image
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [FileInline]
    # exclude = ['main_image', 'load_files']

    def save_related(self, request, form, formsets, change):

        print(self.get_inline_instances(request))
        post = form.instance

        post.load_files.clear()

        image_formset = formsets[0]
        if image_formset.cleaned_data:
            images_data = image_formset.cleaned_data
            print(images_data)
            post.main_image = images_data[0]['upload_image']
            post.save()

            for image_data in images_data:

                if image_data:
                    print(image_data.get('upload_image'))
                    print(Image.objects.filter(upload_image=image_data.get('upload_image')))
                    # print(Image.objects.all().values('upload_image'))
                    image = Image(post_rel=post, upload_image=image_data.get('upload_image'))
                    image.save()
                    post.load_files.add(image)

            super().save_related(request, form, formsets, change)


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Reply)
admin.site.register(Category)
admin.site.register(Image)
