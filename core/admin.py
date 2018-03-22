from django.contrib import admin
from django.contrib.auth.models import Group, User

from core.models import Article, Site


admin.site.site_header = 'MLCrawler Administration'
admin.site.site_title = 'MLCrawler'

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    readonly_fields = ('name', 'main_url')
    list_display = ('name', 'main_url')

    def has_add_permission(self, request):
        return False


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp', 'site')
    list_filter = ('site',)

    def has_add_permission(self, request):
        return False
