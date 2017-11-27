import markdown
from django.contrib.auth.models import User
from django.db import models
# 分类
from django.urls import reverse
from django.utils.html import strip_tags


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
    views = models.PositiveIntegerField(default=0)  # 文章浏览数

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                               'markdown.extensions.codehilite', ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]  # strip_tags 去掉 HTML 文本的全部 HTML 标签
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-create_time']  # 默认按照 create_time 降序排列


