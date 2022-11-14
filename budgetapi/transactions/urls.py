from django.urls import path

from .views import TransactionDetail, TransactionList, TransactionStats


urlpatterns = [
    path("<int:pk>/", TransactionDetail.as_view(), name="transaction_detail"),
    path("", TransactionList.as_view(), name="transaction_list"),
    path("stats/", TransactionStats.as_view(), name="transaction_list"),
]
