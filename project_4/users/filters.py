import django_filters
from auction_store.models import Item, Bid
from django.db.models import Q


class SaleHistoryFilter(django_filters.FilterSet):

    SALE_CHOICES = (
        ('newest', 'Newest'),
        ('oldest', 'Oldest'),
        ('low_price', 'Low Price'),
        ('high_price', 'High Price')
    )

    sale = django_filters.ChoiceFilter(
        label='', choices=SALE_CHOICES, method='filter_by_sale')

    multi_name_fields = django_filters.CharFilter(label='',
                                                  method='filter_by_all_name_fields')

    class Meta:
        model = Item
        fields = ['price', 'name',
                  'price', 'seller', 'buyer']

    def filter_by_sale(self, queryset, name, value):
        if value == 'newest':
            x = '-start_date'
        elif value == 'oldest':
            x = 'start_date'
        elif value == 'high_price':
            x = '-price'
        elif value == 'low_price':
            x = 'price'
        return queryset.order_by(x)


class PurchaseHistoryFilter(django_filters.FilterSet):

    PURCHASE_CHOICES = (
        ('newest', 'Newest'),
        ('oldest', 'Oldest'),
        ('low_price', 'Low Price'),
        ('high_price', 'High Price')
    )

    purchase = django_filters.ChoiceFilter(
        label='', choices=PURCHASE_CHOICES, method='filter_by_purchase')


    class Meta:
        model = Item
        fields = ['sold_price', 'name',
                  'price', 'seller', 'buyer']

    def filter_by_purchase(self, queryset, name, value):
        if value == 'newest':
            x = '-sold_date'
        elif value == 'oldest':
            x = 'sold_date'
        elif value == 'high_price':
            x = '-sold_price'
        elif value == 'low_price':
            x = 'sold_price'
        return queryset.order_by(x)


class BidHistoryFilter(django_filters.FilterSet):

    BID_SORT_CHOICES = (
        ('newest', 'Newest'),
        ('oldest', 'Oldest'),
        ('low_bid', 'Low Bid'),
        ('high_bid', 'High Bid')
    )

    bid_sort = django_filters.ChoiceFilter(
        label='', choices=BID_SORT_CHOICES, method='filter_by_bid_sort')

    class Meta:
        model = Bid
        fields = ['amount', 'date', 'bidder']

    def filter_by_bid_sort(self, queryset, name, value):
        if value == 'newest':
            x = '-date'
        elif value == 'oldest':
            x = 'date'
        elif value == 'high_bid':
            x = '-amount'
        elif value == 'low_bid':
            x = 'amount'
        return queryset.order_by(x)
