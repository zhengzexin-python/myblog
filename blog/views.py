from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Post, Category
from comments.forms import CommentForm
import markdown


# 首页视图
def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})


# 文章视图
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()  # 文章浏览数加1
    # 使用markdown进行渲染
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # 语法高亮拓展
        'markdown.extensions.toc',
    ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request, 'blog/detail.html', context=context)


# 归档视图
def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by("-create_time")
    return render(request, template_name='blog/index.html', context={"post_list": post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', {'post_list': post_list})
