from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Post, Category
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
import markdown


# 首页视图
class IndexView(ListView):
    model = Post  # 设置获取的model
    template_name = 'blog/index.html'  # 设置模板
    context_object_name = 'post_list'  # 设置返回的变量名


# 文章视图
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc'
        ])
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


# 归档视图
class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')  # 获取 url 中的year参数
        month = self.kwargs.get('month')  # 获取 url 中的month参数
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year,
                                                               create_time__month=month)


# 分类视图
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
