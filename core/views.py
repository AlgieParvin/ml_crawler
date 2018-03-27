from django.views.generic import ListView

from core.models import Article, Site
from .sites import sites_info, ALL


ARTICLES_PER_PAGE = 20
PAGES_TO_DISPLAY = 5


class ArticleListView(ListView):
    template_name = 'core/base.html'
    paginate_by = ARTICLES_PER_PAGE

    def get_queryset(self):
        slug, period = sites_info[0]['slug'], ALL
        try:
            slug = self.kwargs['slug']
            period = self.kwargs['period']
        except KeyError:
            pass
        site_name = Site.objects.get(slug=slug)
        return Article.query_articles(site_name, period)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        slug, period = sites_info[0]['slug'], ALL
        try:
            slug = self.kwargs['slug']
            period = self.kwargs['period']
        except KeyError:
            pass

        if context['is_paginated']:
            page_index = context['page_obj'].number
            start_page = page_index - (PAGES_TO_DISPLAY - 1) \
                if page_index % PAGES_TO_DISPLAY == 0 \
                else page_index - (page_index % PAGES_TO_DISPLAY) + 1
            end_page = min(start_page + PAGES_TO_DISPLAY - 1, context['paginator'].num_pages)
            pages = list(range(start_page, end_page + 1))
            context.update({
                'pages': pages,
                'current_page': page_index,
                'next_page_to_scroll': end_page + 1,
                'previous_page_to_scroll': start_page - 1,
                'has_previous_pages': start_page != 1,
                'has_next_pages': end_page < context['paginator'].num_pages,
                'many_pages': context['paginator'].num_pages > 1
            })

        sites = Site.objects.all()
        current_site = Site.objects.get(slug=slug)
        articles_counter = Article.articles_counters_for_periods(current_site.name)
        context.update({
            'sites': sites,
            'current_site': current_site,
            'periods': articles_counter,
            'period': period
        })
        return context
