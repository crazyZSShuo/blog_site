from django.contrib.syndication.views import Feed
from django.urls import reverse


from blog.models import Article



class LatestEntriesFeed(Feed):
    title = 'CrazyZs_Blog News'
    link = '/rss'
    description = 'CrazyZs_Blog 站点文章更新'

    # 数据
    def items(self):
        return Article.objects.order_by('-article_create_time')

    # 标题
    def item_title(self,item):
        return item.article_title

    # 简介
    def item_description(self, item):
        return item.article_synopsis

    # 生成链接
    def item_link(self, item):
        return reverse('blog',args=[item.pk])