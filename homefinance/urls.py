from django.urls import path, include
from homefinance.views import HomeView, TransactionHistoryView, AddExpenseView, AddIncomeView, EditExpenseView, EditIncomeView, DeleteTransactionView

budget_patterns = [
    path('add_expense', AddExpenseView.as_view(), name='add_expense'),
    path('edit_expense/<int:transaction_id>', EditExpenseView.as_view(), name='edit_expense'),
    path('add_income', AddIncomeView.as_view(), name='add_income'),
    path('edit_income/<int:transaction_id>', EditIncomeView.as_view(), name='edit_income'),
    path('delete_transaction/<int:transaction_id>', DeleteTransactionView.as_view(), name='delete_transaction'),
    path('transaction_history', TransactionHistoryView.as_view(), name='transaction_history'),
]


urlpatterns = [
    path('', HomeView.as_view(), name='base'),
    path('<int:budget_id>/', include(budget_patterns)),
]
