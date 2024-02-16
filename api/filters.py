from django.db.models import QuerySet, Count
from rest_framework import filters
from rest_framework.request import Request


class ChoiceCountFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_choice_count = request.query_params.get('min_choice_count')
        max_choice_count = request.query_params.get('max_choice_count')
        if min_choice_count is not None and max_choice_count is not None:
            queryset = queryset \
                .annotate(choice_count=Count('choices'))\
                .filter(choice_count__gte=min_choice_count) \
                .filter(choice_count__lte=max_choice_count)
        return queryset


class ArticleTextFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_article_text_length = request.query_params.get('min_article_text_length')
        max_article_text_length = request.query_params.get('max_article_text_length')
        if min_article_text_length is not None and max_article_text_length is not None:
            queryset = queryset \
                .annotate(choice_count=Count('article'))\
                .filter(choice_count__gte=min_article_text_length) \
                .filter(choice_count__lte=max_article_text_length)
        return queryset

