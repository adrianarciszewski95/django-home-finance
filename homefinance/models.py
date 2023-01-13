from django.db import models
from django.contrib.auth.models import User

class Budget(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=100, blank=True, null=True)
    shared_with = models.ManyToManyField(User, related_name='shared_budgets', blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    TYPES = [
        ('Expense', 'Expense'),
        ('Income', 'Income')
    ]
    type = models.CharField (choices=TYPES, max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"

class Transaction(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_income = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk} - {self.budget} - {self.category} - {self.amount}"

class SavingGoal(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deadline = models.DateField()

    def __str__(self):
        return self.name

