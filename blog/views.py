from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Post, Category, Tag
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
import markdown


# 首页视图
class IndexView(ListView):
    model = Post  # 设置获取的model
    template_name = 'blog/index.html'  # 设置模板
    context_object_name = 'post_list'  # 设置返回的变量名
    paginate_by = 1  # 设置分页大小

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        # 如果没有分页, 返回空字典
        if not is_paginated:
            return {}
        left = []  # 左边连续页码
        right = []  # 右边连续页码
        left_has_more = False  # 标示第 1 页页码后是否需要显示省略号
        right_has_more = False  # 标示最后一页页码前是否需要显示省略号
        first = False  # 标示是否需要显示第 1 页的页码号
        last = False  # 标示是否需要显示最后一页的页码号
        page_number = page.number  # 用户请求的页码
        total_pages = paginator.num_pages  # 总页数
        page_range = paginator.page_range  # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page_number == total_pages:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            right = page_range[page_number:page_number + 2]
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0: page_number - 1]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


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


# 云标签视图
class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
