from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger # 翻页相关模块
from django.db.models import Q # 模糊查询多个字段使用


from .models import Article,Category,UserProfile,Acimage,Siteinfo
from .forms import Searchform,Tagform

# Create your views here.


# 博客列表
def bloglist(request):
    articles = Article.objects.filter(article_type='2').order_by('-article_create_time')
    # 获取当前页码，用来控制翻页中当前页面的class="{% if p==page_number %}am-active {% endif %}"
    c = request.GET.get('c','') # 分类
    page_number = int(request.GET.get('p','1')) # 页数
    s = '' # 搜索关键字
    t = '' # tag关键字
    d = request.GET.get('d','')  # 默认文章归档

    if request.method == 'GET':
        form = Searchform(request.GET)
        if form.is_valid():
            s = request.GET.get('s')

    if request.method == 'GET':
        form = Tagform(request.GET)
        if form.is_valid():
            t  = request.GET.get('t')

    if c:
        # 分类页
        articles = articles.filter(article_category=c,article_type='2').order_by('-article_create_time')
    elif s:
        # 搜索结果
        articles = articles.filter(Q(article_title__contains=s) | Q(article_content__contains=s),
                                   article_type='2').order_by('-article_create_time')
    elif t:
        # 标签搜索结果
        articles = articles.filter(article_tag__contains=t,article_type='2').order_by('-article_create_time')
    elif d:
        # 文章归档，创建时间对象，取年，月，用filter取相关时间的日志
        md = datetime.strptime(d,'%Y-%m')
        articles = articles.filter(article_create_time__year=md.year,article_create_time__month=md.month,article_type='2')

    paginator = Paginator(articles,8) # 分页，第一个参数为文章列表，第二个参数为每页展示多少条
    page = request.GET.get('p') # 获取url中的页码
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger: # 若不是整数，则跳到第一页
        contacts = paginator.page(1)
    except EmptyPage: # 若超过了最后一页
        contacts = paginator.page(paginator.num_pages)

    # 优化数据翻页
    pages = pagesHelp(page,paginator.num_pages,6)
    page_url = request.get_full_path()
    return render(request,'blog/list.html',{
        'articles':articles,
        'contacts':contacts,
        'c':c,
        's':s,
        'd':d,
        't':t,
        'page_url':page_url,
        'page_number':page_number,
        'form':form,
        'pages':pages,
    })

def pagesHelp(page,num_pages,maxpage):
    '''
    Paginator Django数据分页优化,使数据分页列表显示规定的页数
    :param page: 当前页码
    :param num_pages: 总页数
    :param maxpage: 列表显示最多页数
    :return:
    '''
    if page is None:
        p = 1
    else:
        p = int(page)
    offset = num_pages - p
    if num_pages > maxpage and offset <= maxpage and p >= maxpage:
        # 假设100页 100-98=2,页尾处理
        # 结果小于规定数但是当前页大于规定页数
        # print("结果小于规定数但是当前页大于规定页数",[i + 1 for i in range(num_pages - maxpage, num_pages)])
        return [i + 1 for i in range(num_pages - maxpage, num_pages)]

    elif num_pages > maxpage and offset >= maxpage and p <= maxpage:
        # 假设100页 100-2=98，页头
        # 结果小于规定数但是当前页大于规定页数
        # print("结果小于规定数但是当前页大于规定页数",[i + 1 for i in range(maxpage)])
        return [i + 1 for i in range(maxpage)]

    elif num_pages <= maxpage:
        # 假设3页  3<6，总页数很少，少于规定页数
        # 当前页码数小于规定数
        # print("当前页码数小于规定数",[i + 1 for i in range(num_pages)])
        return [i + 1 for i in range(num_pages)]
    else:
        # 正常页数分配
        # print("正常页数分配",[i + 1 for i in range(p - int(maxpage / 2), p + int(maxpage / 2))])
        return [i + 1 for i in range(p - int(maxpage / 2), p + int(maxpage / 2))]



# 文章详情页
def blog(request,id):
    article = Article.objects.get(pk=id)
    article.increase_article_click() # 增加访问量

    # 检测上一篇和下一篇文章
    try:
        pa = Article.objects.get(pk=int(id)-1) # 前一篇
        if pa.article_type != '2':
            pa=None
    except Exception as e:
        pa = None

    try:
        na = Article.objects.get(pk=int(id)+1) # 后一篇
        if na.article_type != '2':
            na = None
    except Exception as e:
        na = None

    # userinfo = UserProfile.objects.get(pk=1)#站长资料
    # categorys = Category.objects.all()#获取所有分类
    # siteinfo = Siteinfo.objects.get(pk=1)#获取站点信息
    tags = article.article_tag.split(',')

    if article.article_type != '2':
        return render(request,'404.html')
    else:
        return render(request,'blog/blog.html',{
            'article':article,
            'pa':pa,
            'na':na,
            # 'userinfo':userinfo,
            # 'categorys':categorys,
            # 'siteinfo':siteinfo,
            'tags':tags,
        })


def page_not_found(request):
    return render(request,'404.html')

def page_error(request):
    return render(request,'500.html')

def permission_denied(request):
    return render(request,'403.html')


def test(request):
    values = request.META.items()
    html = []
    for k,v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>'%(k,v))
    return HttpResponse('<table>%s</table>'%'\n'.join(html))


def robots(request):
    return HttpResponse('User-Agent:*')


# 站点地图
def sitemap(request):
    articles = Article.objects.filter(article_type='2').order_by('-article_create_time')
    return render(request,'sitemap.html',{'articles':articles},content_type='text/xml')



