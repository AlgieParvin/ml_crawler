from django.contrib import admin
from core.models import Article, Site


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
