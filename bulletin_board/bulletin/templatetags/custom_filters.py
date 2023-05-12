from django import template

register = template.Library()


@register.filter(name='get_media_ext')
def get_media_ext(value, queryset):
    return value.upload_file.name.split('.')[-1] in queryset
