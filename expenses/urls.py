# expenses/urls.py
from django.urls import path
from .views import ExpenseListView, AddExpenseView, DeleteExpenseView, ConfirmDeleteExpensesView, GetTransactionsView, AddTransactionView, ChartView, DeleteUserTransactionsView, TransactionListView

urlpatterns = [
    path('expenses/', ExpenseListView.as_view(), name='expense_list'),
    path('expenses/<int:year>/<int:month>/', ExpenseListView.as_view(), name='expense_list_month'),
    path('add/', AddExpenseView.as_view(), name='add_expense'),
    path('delete/', ConfirmDeleteExpensesView.as_view(), name='confirm_delete_expenses'),
    path('delete/all/', ConfirmDeleteExpensesView.as_view(), name='delete_all_expenses'),
    path('expenses/<int:expense_id>/delete/', DeleteExpenseView.as_view(), name='delete_expense'),

# Dashboard Financeiro
    path("chart/", ChartView.as_view(), name='chart'),
    path("transactions/", GetTransactionsView.as_view(), name="get_transactions"),
    path("transactions/add/", AddTransactionView.as_view(), name="add_transaction"),
    path("api/transactions/", GetTransactionsView.as_view(), name="api_get_transactions"),
    path("api/transactions/add/", AddTransactionView.as_view(), name="api_add_transaction"),
    path("api/transactions/delete/", DeleteUserTransactionsView.as_view(), name="api_delete_transactions"),
    path('api/transactions/', TransactionListView.as_view(), name='get_transactions'),
]
