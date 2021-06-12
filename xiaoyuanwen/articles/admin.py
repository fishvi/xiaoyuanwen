from django.contrib import admin

from xiaoyuanwen.articles.models import Article
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    '''设置列表可显示的字段'''
    list_display = ('title', )

    '''设置过滤选项'''
    list_filter = ()

    '''每页显示条目数'''
    list_per_page = 5

    '''设置可编辑字段'''
    list_editable = ()

    '''按发布日期排序'''
    ordering = ()


admin.site.register(Article, ArticleAdmin)
