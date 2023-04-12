from django.contrib import admin
from .models import *
from django import forms


class FileInline(admin.TabularInline):
    model = Image
    extra = 1


class PostAdmin(admin.ModelAdmin):
    # fields = ('author', 'title', 'content', 'category', '')
    inlines = [FileInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.load_files.set(form.cleaned_data['load_files'])
        form.instance.save()


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Reply)
admin.site.register(Category)
admin.site.register(Image)
