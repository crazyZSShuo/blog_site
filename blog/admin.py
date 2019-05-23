from django.contrib import admin
from django.utils.safestring import mark_safe
# Register your models here.

from .models import UserProfile,Article,Category,Siteinfo,Acimage



class UserProfileAdmin(admin.ModelAdmin):
    # 后台显示字段
    list_display = ['username','user_nick_name','user_detail','email','user_gender','user_mobile','user_address']

    # 过滤器设置
    list_filter = ('username','user_nick_name','email')

    # 搜索字段
    search_fields = ('username','user_nick_name','email')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name','category_detail','category_sort_id']
    list_filter = ('category_name','category_sort_id')


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['article_title','article_user','article_category','article_type','article_up','article_support','article_click']

    # 设置每页显示多少条记录，默认为100条
    list_per_page = 15
    list_filter = ('article_category','article_create_time')
    search_fields = ('article_title',)
    date_hierarchy = 'article_create_time' # 详细时间分层筛选



class SiteinfoAdmin(admin.ModelAdmin):
    list_display = ['site_name','site_user','site_detail']


class AcimageAdmin(admin.ModelAdmin):
    list_display = ['image_title','image_detail','image_url','image_data']
    readonly_fields = ('image_data','image_url')

    def image_url(self,obj):
        return mark_safe('<a g=href="%s">右键复制图片地址</a>'%obj.image_path.url)
    def image_data(self,obj):
        img = mark_safe('<img src="%s" width="100px" />'%obj.image_path.url)
        return img

    # 页面显示的字段名称
    image_data.short_description = '图片'
    image_url.short_description = '图片地址'


admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Siteinfo,SiteinfoAdmin)
admin.site.register(Acimage,AcimageAdmin)