from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Budget, Transaction, Category
from .forms import TransactionForm
from .mixins import UserBudgetsMixin


class HomeView(UserBudgetsMixin, View):
    def get(self, request):
        return render(request, 'home.html', {'budgets': self.budgets})

class TransactionHistoryView(UserBudgetsMixin, View):
    def get(self, request, budget_id):

        transactions = Transaction.objects.filter(budget__id=budget_id).order_by('-date')

        # filter by date
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)

        # filter by type
        type = request.GET.get('type')
        if type:
            transactions = transactions.filter(is_income=(type == 'Income'))

        return render(request, 'transaction_history.html', {'transactions': transactions, 'budgets': self.budgets})


class AddExpenseView(UserBudgetsMixin, View):
    def get(self, request, budget_id):
        form = TransactionForm()
        form.fields['category'].queryset = Category.objects.filter(type='Expense')
        return render(request, 'add_expense.html', {'budgets': self.budgets, 'form': form, 'new': True})

    def post(self, request, budget_id):
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.budget = Budget.objects.get(id=budget_id)
                transaction.save()
                return redirect('base')

class AddIncomeView(UserBudgetsMixin, View):
    def get(self, request, budget_id):
        form = TransactionForm()
        form.fields['category'].queryset = Category.objects.filter(type='Income')
        return render(request, 'add_income.html', {'budgets': self.budgets, 'form': form, 'new': True})

    def post(self, request, budget_id):
            form = TransactionForm(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.budget = Budget.objects.get(id=budget_id)
                transaction.is_income = True
                transaction.save()
                return redirect('base')

class EditExpenseView(UserBudgetsMixin, View):
    def get(self, request, budget_id, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        form = TransactionForm(instance=transaction)
        form.fields['category'].queryset = Category.objects.filter(type='Expense')
        return render(request, 'add_expense.html', {'budgets': self.budgets, 'form': form, 'new': False})

    def post(self, request, budget_id, transaction_id):
            transaction = get_object_or_404(Transaction, pk=transaction_id)
            form = TransactionForm(request.POST, instance=transaction)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.save()
                return redirect('base')

class EditIncomeView(UserBudgetsMixin, View):
    def get(self, request, budget_id, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        form = TransactionForm(instance=transaction)
        form.fields['category'].queryset = Category.objects.filter(type='Income')
        return render(request, 'add_income.html', {'budgets': self.budgets, 'form': form, 'new': False})

    def post(self, request, budget_id, transaction_id):
            transaction = get_object_or_404(Transaction, pk=transaction_id)
            form = TransactionForm(request.POST, instance=transaction)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.save()
                return redirect('base')

class DeleteTransactionView(UserBudgetsMixin, View):
    def get(self, request, budget_id, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        return render(request, 'confirm_delete.html', {'budgets': self.budgets, 'budget_id': budget_id})

    def post(self, request, budget_id, transaction_id):
            transaction = get_object_or_404(Transaction, pk=transaction_id)
            transaction.delete()
            return redirect('base')




