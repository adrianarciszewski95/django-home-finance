from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from.models import Budget, Transaction

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['name', 'password', 'balance']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'category', 'description', 'amount']



