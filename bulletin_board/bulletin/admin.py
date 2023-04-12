from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Posts)
admin.site.register(Reply)
admin.site.register(Category)
