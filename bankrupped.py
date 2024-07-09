class WithdrawMoneyView(TransactionCreateMixin):
  form_class = WithDrawForm
  title = 'Withdraw'

  def get_initial(self):
    initial  = {'transaction_type': 'withdraw'}
    return initial
  
  def form_valid(self, form):
    amount = form.cleaned_data['amount']
    account = self.request.user.account
    bank_balance = UserAccount.objects.aggregate(total_balance=Sum("balance"))[
            "total_balance"
    ]

    if bank_balance < amount:
      messages.warning(self.request, "Bank is bankruped")
    else:
      account.balance -= amount

      account.save(
        update_fields = ['balance']
      )

      send_mail_to_user(
        "Withdraw message",
        self.request.user,
        amount,
        'transactions/withdraw_email.html'
      )

      messages.success(self.request, f'{amount} was withdrawn from your account successfully.')

    return super().form_valid(form)