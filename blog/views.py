from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Post, Category
import markdown


# 首页视图
def index(request):
    post_list = Post.objects.all().order_by("-create_time")
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 文章视图
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 使用markdown进行渲染
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # 语法高亮拓展
        'markdown.extensions.toc',
    ])
    return render(request, 'blog/detail.html', context={'post': post})


# 归档视图
def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by("-create_time")
    return render(request, template_name='blog/index.html', context={"post_list": post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by("-create_time")
    return render(request,'blog/index.html',{'post_list': post_list})
