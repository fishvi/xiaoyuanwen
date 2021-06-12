from django.contrib import admin

from xiaoyuanwen.news.models import News
# Register your models here.


class NewsAdmin(admin.ModelAdmin):
    pass


admin.site.register(News, NewsAdmin)
