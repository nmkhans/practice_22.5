class BalanceTransferView(TransactionCreateMixin):
  form_class = BalanceTransferForm
  template_name = 'transactions/transfer_money.html'
  title = "Transfer Balance"
  success_url = reverse_lazy('transaction-report')

  def get_initial(self):
    initial = {'transaction_type': 'balance-transfer'}
    return initial
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.update({
      'title': self.title
    })

    return context
  
  def form_valid(self, form):
    amount = form.cleaned_data['amount']
    reciver_username = form.cleaned_data['reciver']

    user_account = self.request.user.account
    try:
      reciver_user = User.objects.get(username = reciver_username)
      reciver_user_account = UserAccount.objects.get(user = reciver_user)

      user_account.balance -= amount
      reciver_user_account.balance += amount

      reciver_user_account.save()
      user_account.save()

      messages.success(self.request, 'Balance has been transfered.')

      send_mail_to_user(
        "Balance transfer",
        self.request.user,
        amount,
        'transactions/balance_transfer_email.html'
      )

      send_mail_to_user(
      "Deposit message",
      reciver_user,
      amount,
      'transactions/deposit_email.html'
    )

      return super().form_valid(form)
    
    except User.DoesNotExist:
      form.add_error('reciver', "User does not exist.")
      return super().form_invalid(form)