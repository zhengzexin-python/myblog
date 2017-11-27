from django.contrib.syndication.views import Feed

from blog.models import Post


class AllPostsRssFeed(Feed):
    title = 'django 博客系统'  # 显示在聚合阅读器上的标题
    link = '/'  # 通过聚合阅读器跳转到网站的地址
    description = 'django 博客系统测试'  # 显示在聚合阅读器上的描述信息

    # 需要显示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # 聚合器中显示的内容条目的描述
    def item_description(self, item):
        return item.body
