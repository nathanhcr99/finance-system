from django.urls import path
from .views import TransactionList,AccountDetail,AccountList,TransactionCategoryList,TransactionDetail


urlpatterns = [
    path('transacoes/', TransactionList.as_view(), name='lista-transacoes'),
    path('contas/', AccountList.as_view(), name='lista-contas'),
    path('contas/<int:pk>/', AccountDetail.as_view(), name='detalhes-contas'),
    path('categoria-transacoes/', TransactionCategoryList.as_view(), name='lista-categoria-transacoes'),
    path('transacao/<int:pk>/', TransactionDetail.as_view(), name='detalhes-transacoes'),


]
