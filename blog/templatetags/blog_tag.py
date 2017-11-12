from blog.models import Post, Category
from django import template

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
    return Category.objects.all()