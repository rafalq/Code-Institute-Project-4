import django_filters
from .models import *
# from django.utils import timezone
# import datetime


class ItemFilter(django_filters.FilterSet):

    # price = django_filters.NumberFilter()
    price_g = django_filters.NumberFilter(label='€ Price',
                                          field_name='price', lookup_expr='gt')
    price_l = django_filters.NumberFilter(label='Range',
                                          field_name='price', lookup_expr='lt')

    # price = django_filters.NumberFilter(
    #     label='Price (less than)', lookup_expr='lt')

    FORMAT_CHOICES = (
        ('all', 'All Listings'),
        ('auction', 'Auction'),
        ('end_auction', 'Ended Auction'),
        ('sale', 'Only Sale'),
        ('sold', 'Sold')
    )
    format = django_filters.ChoiceFilter(
        label="Buying Format", choices=FORMAT_CHOICES, method='filter_by_format')

    SORT_CHOICES = (
        ('newest', 'Newest'),
        ('oldest', 'Oldest'),
        ('low_price', 'Low Price'),
        ('high_price', 'High Price'),
    )

    sort = django_filters.ChoiceFilter(
        label="Sort", choices=SORT_CHOICES, method='filter_by_sort')

    class Meta:
        model = Item
        fields = ['category', 'price']

    def filter_by_sort(self, queryset, name, value):
        if value == 'newest':
            x = '-start_date'
        elif value == 'oldest':
            x = 'start_date'
        elif value == 'high_price':
            x = '-price'
        elif value == 'low_price':
            x = 'price'
        return queryset.order_by(x)

    def filter_by_format(self, queryset, name, value):

        if value == 'auction':
            queryset = queryset.filter(
                end_date__gte=timezone.now(), in_auction=True, sold=False)
        elif value == 'end_auction':
            queryset = queryset.filter(
                end_date__lt=timezone.now(), sold=False, in_auction=True)
        elif value == 'sale':
            queryset = queryset.filter(
                sold=False, winner__isnull=True, end_date__lt=timezone.now())
        elif value == 'sold':
            queryset = queryset.filter(sold=True)
        else:
            queryset = queryset.all()
        return queryset
