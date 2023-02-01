from django.urls import path, include
from homefinance.views import user_signup, user_login, user_logout, MainView, CreateBudgetView, AddExpenseView, AddIncomeView, EditExpenseView, EditIncomeView, DeleteTransactionView, TransactionHistoryView, BudgetAnalyseView

budget_patterns = [
    path('add_expense', AddExpenseView.as_view(), name='add_expense'),
    path('edit_expense/<int:transaction_id>', EditExpenseView.as_view(), name='edit_expense'),
    path('add_income', AddIncomeView.as_view(), name='add_income'),
    path('edit_income/<int:transaction_id>', EditIncomeView.as_view(), name='edit_income'),
    path('delete_transaction/<int:transaction_id>', DeleteTransactionView.as_view(), name='delete_transaction'),
    path('transaction_history', TransactionHistoryView.as_view(), name='transaction_history'),
    path('budget_analyse/<int:year>/<int:month>', BudgetAnalyseView.as_view(), name = 'budget_analyse')
]


urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('signup', user_signup, name='user_signup'),
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout"),
    path('create_budget', CreateBudgetView.as_view(), name='create_budget' ),
    path('<int:budget_id>/', include(budget_patterns)),
]
