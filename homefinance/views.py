from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .models import Budget, Transaction, Category
from .forms import SignUpForm, BudgetForm, TransactionForm
from .mixins import SidebarMixin

def user_signup(request):
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect('main')
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = SignUpForm()
	return render (request, 'signup.html', {'register_form':form})

def user_login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect('main')
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, 'login.html', {"login_form":form})

def user_logout(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect('login')

class MainView(SidebarMixin, View):
    def get(self, request):
        return render(request, 'main.html', {'budgets': self.budgets, 
                                            'current_month': self.current_month, 
                                            'current_year': self.current_year})


class CreateBudgetView(SidebarMixin, View):
    def get(self, request):
        form = BudgetForm()
        return render(request, 'create_budget.html', {'budgets': self.budgets, 
                                                    'current_month': self.current_month, 
                                                    'current_year': self.current_year,
                                                    'form': form, 
                                                    })
    def post(self, request):
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('main')

class AddExpenseView(SidebarMixin, View):
    def get(self, request, budget_id):
        form = TransactionForm()
        form.fields['category'].queryset = Category.objects.filter(type='Expense')
        return render(request, 'add_expense.html', {'budgets': self.budgets, 
                                                    'current_month': self.current_month, 
                                                    'current_year': self.current_year,
                                                    'form': form, 
                                                    'new': True
                                                    })
    def post(self, request, budget_id):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.budget = Budget.objects.get(id=budget_id)
            transaction.save()
            return redirect('main')

class AddIncomeView(SidebarMixin, View):
    def get(self, request, budget_id):
        form = TransactionForm()
        form.fields['category'].queryset = Category.objects.filter(type='Income')
        return render(request, 'add_income.html', {'budgets': self.budgets, 
                                                    'current_month': self.current_month, 
                                                    'current_year': self.current_year,
                                                    'form': form, 
                                                    'new': True
                                                     })

    def post(self, request, budget_id):
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.budget = Budget.objects.get(id=budget_id)
            transaction.is_income = True
            transaction.save()
            return redirect('main')

class EditExpenseView(SidebarMixin, View):
    def get(self, request, budget_id, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        form = TransactionForm(instance=transaction)
        form.fields['category'].queryset = Category.objects.filter(type='Expense')
        return render(request, 'add_expense.html', {'budgets': self.budgets, 
                                                    'current_month': self.current_month, 
                                                    'current_year': self.current_year,
                                                    'form': form, 
                                                    'new': False
                                                    })

    def post(self, request, budget_id, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            return redirect('main')

class EditIncomeView(SidebarMixin, View):
    def get(self, request, budget_id, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        form = TransactionForm(instance=transaction)
        form.fields['category'].queryset = Category.objects.filter(type='Income')
        return render(request, 'add_income.html', {'budgets': self.budgets, 
                                                    'current_month': self.current_month, 
                                                    'current_year': self.current_year,
                                                    'form': form, 
                                                    'new': False
                                                    })

    def post(self, request, budget_id, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            return redirect('main')

class DeleteTransactionView(SidebarMixin, View):
    def get(self, request, budget_id, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        return render(request, 'confirm_delete.html', {'budgets': self.budgets, 
                                                        'current_month': self.current_month, 
                                                        'current_year': self.current_year,
                                                        'budget_id': budget_id, 
                                                        })

    def post(self, request, budget_id, transaction_id):
            transaction = get_object_or_404(Transaction, pk=transaction_id)
            transaction.delete()
            return redirect('main')


class TransactionHistoryView(SidebarMixin, View):
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

        return render(request, 'transaction_history.html', {'budgets': self.budgets, 
                                                            'current_month': self.current_month, 
                                                            'current_year': self.current_year,
                                                            'transactions': transactions
                                                            })


class BudgetAnalyseView(SidebarMixin, View):       
    def get(self, request, budget_id, year, month):
        transactions = Transaction.objects.filter(budget__id = budget_id, date__year = year, date__month = month)
        income_sum = round(transactions.filter(is_income = True).aggregate(Sum('amount'))['amount__sum'] or 0, 2)
        expense_sum = round(transactions.filter(is_income = False).aggregate(Sum('amount'))['amount__sum'] or 0, 2)
        balance = income_sum - expense_sum

        expense_categories = Category.objects.filter(type='Expense')
        expenses = transactions.filter(is_income=False).values('category').annotate(amount_sum=Sum('amount'))

        expenses_by_category = []
        for category in expense_categories:
            expense = expenses.filter(category=category.id).first()
            expenses_by_category.append({'category': category.name, 'amount_sum': round(expense['amount_sum'], 2) if expense else 0})

        income_categories = Category.objects.filter(type='Income')
        incomes = transactions.filter(is_income=True).values('category').annotate(amount_sum=Sum('amount'))

        incomes_by_category = []
        for category in income_categories:
            income = incomes.filter(category=category.id).first()
            incomes_by_category.append({'category': category.name, 'amount_sum': round(income['amount_sum'], 2) if income else 0})
        return render(request, 'budget_analyse.html', {'budgets': self.budgets, 
                                                        'current_year': self.current_year,
                                                        'current_month': self.current_month, 
                                                        'budget_id': budget_id, 
                                                        'year': year,
                                                        'month': month,
                                                        'expense_sum': expense_sum,
                                                        'income_sum': income_sum,
                                                        'balance': balance,
                                                        'expenses_by_category': expenses_by_category,
                                                        'incomes_by_category': incomes_by_category
                                                        })

    def post(self, request, budget_id, year, month):
        if request.POST.get('previous_month'):
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        elif request.POST.get('next_month'):
            month += 1
            if month == 13:
                month = 1
                year += 1
        transactions = Transaction.objects.filter(budget__id = budget_id, date__year = year, date__month = month)
        income_sum = round(transactions.filter(is_income = True).aggregate(Sum('amount'))['amount__sum'] or 0, 2)
        expense_sum = round(transactions.filter(is_income = False).aggregate(Sum('amount'))['amount__sum'] or 0, 2)
        balance = income_sum - expense_sum

        expense_categories = Category.objects.filter(type='Expense')
        expenses = transactions.filter(is_income=False).values('category').annotate(amount_sum=Sum('amount'))

        expenses_by_category = []
        for category in expense_categories:
            expense = expenses.filter(category=category.id).first()
            expenses_by_category.append({'category': category.name, 'amount_sum': round(expense['amount_sum'], 2) if expense else 0})

        income_categories = Category.objects.filter(type='Income')
        incomes = transactions.filter(is_income=True).values('category').annotate(amount_sum=Sum('amount'))

        incomes_by_category = []
        for category in income_categories:
            income = incomes.filter(category=category.id).first()
            incomes_by_category.append({'category': category.name, 'amount_sum': round(income['amount_sum'], 2) if income else 0})


        return render(request, 'budget_analyse.html', {'budgets': self.budgets, 
                                                        'current_year': self.current_year,
                                                        'current_month': self.current_month,
                                                        'budget_id': budget_id, 
                                                        'year': year,
                                                        'month': month,
                                                        'expense_sum': expense_sum,
                                                        'income_sum': income_sum,
                                                        'balance': balance,
                                                        'expenses_by_category': expenses_by_category,
                                                        'incomes_by_category': incomes_by_category
                                                        })

        






