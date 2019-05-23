from random import shuffle
import datetime


from blog.models import UserProfile,Category,Article,Siteinfo

def site_info(request):
    '''站长资料，网站资料，所有分类上下文'''
    userinfo = UserProfile.objects.get(pk=1)
    siteinfo = Siteinfo.objects.get(pk=1)
    categorys = Category.objects.all().order_by('category_sort_id')

    hot_articles = Article.objects.all().order_by('-article_click')[:10] #获取热门文章
    ac_count = Article.objects.count() # 获取文章数量
    d1 = datetime.datetime.now()
    d2 = datetime.datetime(2020,4,20)
    killpy2 = (d2-d1).days
    acs = Article.objects.all()
    ac_click = 0
    for ac in acs:
        ac_click += int(ac.article_click)

    # 根据文章发布的月份进行排序（desc 降序）
    dates =  Article.objects.datetimes('article_create_time','month',order='DESC')

    # 获取文章标签
    l = Article.objects.values('article_tag').distinct().filter(article_type='2')
    tags = []
    for k in l:
        templist = k['article_tag'].split(' ')
        for item in templist:
            if item not in tags:
                tags.append(item)
    shuffle(tags)
    tagcss =['am-radius','am-badge-primary','am-badge-secondary','am-badge-success','am-badge-warning','am-badge-danger']
    return {'userinfo':userinfo, 'siteinfo':siteinfo, 'categorys':categorys,
            'dates':dates, 'alltags':tags, 'tagcss':tagcss,
            'hot_articles':hot_articles,'ac_count':ac_count,'killpy2':killpy2,'ac_click':ac_click,}

