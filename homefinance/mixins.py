from django.contrib.auth.models import User
from .models import Budget

class UserBudgetsMixin:
    def dispatch(self, request, *args, **kwargs):
        self.user = User.objects.get(username = 'ikswezsicra') #temporary until i create a login system
        self.budgets = Budget.objects.filter(user = self.user)
        return super().dispatch(request, *args, **kwargs)

