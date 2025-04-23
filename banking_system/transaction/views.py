from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from transaction.models import Transaction
from .forms import DepositForm,LoanRequestForm,WithdrawForm
from .constrants import DEPOSIT,WITHDRAWAL,LOAN,LOAN_PAID

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'transaction_account': self.request.user.transaction_account
        })
        return kwargs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context.update({
            'title': self.title
        })

        return context

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title ='Deposite'

    def get_initial(self):
        initial = {'transaction_type':DEPOSIT } #deposite =1
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        transaction_account = self.request.user.transaction_account
        transaction_account.balance += amount # amount = 200, tar ager balance = 0 taka new balance = 0+200 = 200
        transaction_account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        return super().form_valid(form)
    

class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}  #Withdraw =2
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.transaction_account.balance -= form.cleaned_data.get('amount')
        # balance = 300
        # amount = 5000
        self.request.user.transaction_account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account'
        )

        return super().form_valid(form)
    

class LoanRequestView(TransactionCreateMixin):
    form_class = LoanRequestForm
    title = 'Request For Loan'

    def get_initial(self):
        initial = {'transaction_type': LOAN}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        current_loan_count = Transaction.objects.filter(
            transaction_account=self.request.user.transaction_account,transaction_type=3,loan_approve=True).count()
        if current_loan_count >= 3:
            return HttpResponse("You have cross the loan limits")
        messages.success(
            self.request,
            f'Loan request for {"{:,.2f}".format(float(amount))}$ submitted successfully'
        )

        return super().form_valid(form)
    
