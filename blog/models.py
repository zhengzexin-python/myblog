from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# 分类
class Category(models.Model):
    name = models.CharField(max_length=100)


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)


# 文章
class Post(models.Model):
    title = models.CharField(max_length=100)  # 标题
    body = models.TextField()  # 文章内容
    create_time = models.DateTimeField()  # 创建时间
    modified_time = models.DateTimeField()  # 最后修改时间
    excerpt = models.CharField(max_length=100, blank=True)  # 文章摘要 允许为空
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)  # 多对多关系 允许标签为空
    author = models.ForeignKey(User)  # 文章作者
