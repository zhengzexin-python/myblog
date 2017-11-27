from blog.models import Post, Category, Tag
from django import template
from django.db.models import Count

register = template.Library()


# 获取最新文章模板标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-create_time")[:num]


# 归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates("create_time", 'month', order='DESC')


# 获得分类模板标签
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 获得标签云模板标签
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
