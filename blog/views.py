from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Post
import markdown


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 使用markdown进行渲染
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',  # 语法高亮拓展
        'markdown.extensions.toc',
    ])
    return render(request, 'blog/detail.html', context={'post': post})
