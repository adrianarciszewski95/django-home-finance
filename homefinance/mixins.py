from django.contrib.auth.models import User
from .models import Budget

from datetime import datetime

class SidebarMixin:
    def dispatch(self, request, *args, **kwargs):
        self.budgets = Budget.objects.filter(user = request.user)
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        return super().dispatch(request, *args, **kwargs)

