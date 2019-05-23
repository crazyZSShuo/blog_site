from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserProfile(AbstractUser):
    GENDER = (
        ('m', '男'),
        ('f', '女'),
        ('o', '保密'),
    )
    user_nick_name = models.CharField(max_length=24, unique=True, verbose_name='昵称')
    user_gender = models.CharField(max_length=10, choices=GENDER, default='o', verbose_name='性别')
    user_birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    user_mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='电话号码')
    user_address = models.CharField(max_length=200, blank=True, null=True, verbose_name='地址')
    user_detail = models.CharField(max_length=200, verbose_name="个人简介", blank=True, null=True)
    user_image = models.ImageField(max_length=100, upload_to='image/user/', default='', verbose_name='用户头像')

    # user_image =  models.ImageField(max_length=100,upload_to='image/user/',verbose_name='用户头像')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']


# 文章分类
class Category(models.Model):
    category_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='分类名称')
    category_detail = models.CharField(max_length=100, blank=True, null=True, verbose_name='分类介绍')
    category_icon = models.CharField(max_length=100, blank=True, null=True, verbose_name='分类图标')
    category_sort_id = models.IntegerField(default=1, verbose_name='分类排序')

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name


# 博客正文文章
class Article(models.Model):
    ART_TYPE = (
        ('0', '草稿'),
        ('1', '软删除'),
        ('2', '正常'),
    )
    ORIGIN_TYPE = (
        ('0', '转载'),
        ('1', '原创'),
    )
    UP_TYPE = (
        ('1', '置顶'),
        ('0', '取消置顶'),
    )
    SUPPORT_TYPE = (
        ('1', '推荐'),
        ('0', '取消推荐'),
    )
    article_title = models.CharField(max_length=50, unique=True, verbose_name='文章标题')
    article_synopsis = models.TextField(blank=True, null=True, verbose_name='简介')
    article_image = models.ImageField(max_length=100, upload_to='image/article/',
                                      default=' ', verbose_name='文章配图')
    # article_image = models.ImageField(max_length=100,upload_to='image/article/',verbose_name='文章配图')
    article_content = models.TextField(blank=True, null=True, verbose_name='文章内容')
    article_user = models.ForeignKey(UserProfile, verbose_name='文章作者')
    article_category = models.ForeignKey(Category, verbose_name='所属分类')
    article_tag = models.CharField(max_length=50, blank=True, null=True, verbose_name='文章标签')
    article_type = models.CharField(max_length=10, choices=ART_TYPE, default='2', verbose_name='文章类别')
    article_original = models.CharField(max_length=10, choices=ORIGIN_TYPE, default='1', verbose_name='是否原创')
    article_click = models.IntegerField(default=0, verbose_name='文章点击率')
    article_up = models.CharField(max_length=10, choices=UP_TYPE, default='1', verbose_name='文章置顶')
    article_support = models.CharField(max_length=10, choices=SUPPORT_TYPE, default='1', verbose_name='文章推荐')
    article_create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.article_title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-article_create_time']

    def increase_article_click(self):
        """
        文章点击量
        :return:
        """
        self.article_click += 1
        self.save()


# 站点信息
class Siteinfo(models.Model):
    site_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='站点名称')
    site_detail = models.CharField(max_length=100, default='', verbose_name='站点介绍')
    site_user = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name='管理员')
    site_logo = models.ImageField(max_length=100, upload_to='image/site/', default=' ',
                                  verbose_name='站点logo')
    # site_logo = models.ImageField(max_length=100,upload_to='image/site/',verbose_name='站点logo')
    site_topimage = models.ImageField(max_length=100, upload_to='image/site/', default=' ',
                                      verbose_name='顶部大图')
    # site_topimage = models.ImageField(max_length=100,upload_to='image/site/',verbose_name='顶部大图')
    site_powered = models.TextField(default='', verbose_name='Powered By')
    site_links = models.TextField(default='', verbose_name='links')
    site_contact = models.TextField(default='', verbose_name='contact Me')
    site_footer = models.TextField(default='', verbose_name='站点底部代码')
    site_changyan = models.TextField(default='', verbose_name='文章底部广告代码')

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = '网站信息'
        verbose_name_plural = verbose_name


class Acimage(models.Model):
    '''相册'''
    image_title = models.CharField(max_length=20, unique=True, verbose_name='图片标题')
    image_detail = models.CharField(max_length=200, blank=True, null=True, verbose_name='图片简介')
    image_path = models.ImageField(max_length=100, upload_to='upload/', default=' ',
                                   verbose_name='图片')

    # image_path =  models.ImageField(max_length=100,upload_to='upload/',verbose_name='图片')

    def __str__(self):
        return self.image_title

    class Meta:
        verbose_name = '网站相册'
        verbose_name_plural = verbose_name
