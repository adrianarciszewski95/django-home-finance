from django.contrib import admin

from .models import Budget, Category, Transaction, SavingGoal

admin.site.register(Budget)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(SavingGoal)

