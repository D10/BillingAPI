from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import BillingViewSet

create_account = BillingViewSet.as_view({
    'post': 'create'
})

make_a_transaction = BillingViewSet.as_view({
    'post': 'transactions'
})

get_account_balance = BillingViewSet.as_view({
    'post': 'get_account_balance'
})

urlpatterns = format_suffix_patterns([
    path('create_account/', create_account),
    path('transaction/', make_a_transaction),
    path('account_balance/', get_account_balance)
])
