from django.contrib import admin

# Register your models here.
from blog.models import Post, Category, Tag
from django.db import models
from pagedown.widgets import AdminPagedownWidget


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'category', 'author']
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget}
    }


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
