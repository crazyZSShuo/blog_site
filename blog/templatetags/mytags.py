from django import template


from markdown import markdown


from ..models import Article,Category
register = template.Library()


# 自定义过滤器
@register.filter
def toMarkdown(str):
    '''markdwn 解析器'''
    return markdown(str)

@register.filter
def cat_count(cat_id):
    '''统计分类下的文章数'''
    return Article.objects.filter(article_category=cat_id).count()
