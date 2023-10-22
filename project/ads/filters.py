from django_filters import FilterSet, CharFilter, ChoiceFilter, filters
from .models import Ad, Reply


class AdsFilter(FilterSet):
    ad_title = CharFilter(lookup_expr='iregex', label="Поиск по названию",)
    class Meta:
        model = Ad

        fields = {'category'}


class RepliesFilter(FilterSet):

    ad__ad_title = CharFilter(label='Объявление', lookup_expr='iregex')

    class Meta:
        model = Reply
        fields = ['is_confirm']
