from django.urls import path

from .views import TransactionDetail, TransactionList


urlpatterns = [
    path("/<int:pk>", TransactionDetail.as_view(), name="transaction_detail"),
    path("", TransactionList.as_view(), name="transaction_list"),
]
