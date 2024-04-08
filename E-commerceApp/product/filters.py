import django_filters

from .models import Product

class ProductsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    keyword = django_filters.filters.CharFilter(field_name="name",lookup_expr="icontains")                # manges us to search about any product name by typing any charchaters can the product name contain
    minPrice = django_filters.filters.NumberFilter(field_name="price" or 0,lookup_expr="gte")             # gte >> grater than or equals
    maxPrice = django_filters.filters.NumberFilter(field_name="price" or 100000,lookup_expr="lte")        # lte >> less than or equals


    class Meta:
        model = Product
      #  fields = ['category', 'brand']
        fields = ('category', 'brand','keyword','minPrice','maxPrice')


























# The distinct=True parameter is used in django_filters to ensure that duplicate results are removed from the queryset after applying the filter.

# In Django, when you perform filtering on a queryset, there might be cases where the filtered queryset contains duplicate records. This can happen if there are multiple related objects that match the filtering criteria, resulting in the same object appearing multiple times in the filtered queryset.

# By default, django_filters doesn't handle duplicate removal. So, if you have multiple related objects that match the filter criteria, all those objects would appear in the filtered queryset, even if they are duplicates.