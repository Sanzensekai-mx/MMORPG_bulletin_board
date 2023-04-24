from django.contrib import admin
from .models import *
from django import forms
from django.db.models.fields.files import ImageFieldFile


class FileInline(admin.TabularInline):
    model = Image
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [FileInline]
    exclude = ['main_image', 'load_files']

    def save_related(self, request, form, formsets, change):
        # print(formsets[0].cleaned_data)
        super().save_related(request, form, formsets, change)
        # print(formsets[0].cleaned_data)
        # print(self.get_inline_instances(request))
        post = form.instance
        image_formset = formsets[0]

        if image_formset.cleaned_data:
            images_data = image_formset.cleaned_data
            # print(images_data)
            post.main_image = images_data[0]['upload_image']
            post.save()

            images = []
            for image_data in images_data:

                if image_data:
                    # print(type(image_data.get('upload_image')))
                    if type(image_data.get('upload_image')) is ImageFieldFile:
                        image = Image.objects.filter(upload_image=image_data.get('upload_image').name).first()
                    else:
                        image = Image.objects.filter(
                            upload_image=f"post_{post.id}/{image_data.get('upload_image').name}").first()
                    images.append(image)

            post.load_files.clear()
            post.load_files.set(images)


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Reply)
admin.site.register(Category)
admin.site.register(Image)
