# expenses/views.py
from .models import Expense, UserProfile
from .forms import ExpenseForm
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from django.http import JsonResponse
from .models import Transaction
import json

# Lista de despesas
class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        year = self.kwargs.get('year', None)
        month = self.kwargs.get('month', None)

        if year is None or month is None:
            current_date = datetime.now()
            year = current_date.year
            month = current_date.month

        return Expense.objects.filter(user=self.request.user, date__year=year, date__month=month)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        year = int(self.kwargs.get('year', datetime.now().year))
        month = int(self.kwargs.get('month', datetime.now().month))

        # Lógica para cálculo do mês anterior e próximo
        prev_month, prev_year = (month - 1, year) if month > 1 else (12, year - 1)
        next_month, next_year = (month + 1, year) if month < 12 else (1, year + 1)

        # Calcular total de despesas e diferenças
        expenses = self.get_queryset()
        total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
        salary = UserProfile.objects.get(user=self.request.user).salary if UserProfile.objects.filter(user=self.request.user).exists() else None
        difference = salary - total_expenses if salary is not None else None

        # Calcular a soma das despesas por categoria
        expenses_by_category = expenses.values('expense_category').annotate(total_amount=Sum('amount'))

        context.update({
            'total_expenses': round(total_expenses, 2),
            'salary': salary,
            'difference': difference,
            'expenses_by_category': expenses_by_category,
            'year': year,
            'month': month,
            'prev_year': prev_year,
            'prev_month': prev_month,
            'next_year': next_year,
            'next_month': next_month,
        })

        return context

    def post(self, request, *args, **kwargs):
        salary = request.POST.get('salary')
        if salary:
            try:
                salary = Decimal(salary)
            except (ValueError, InvalidOperation):
                salary = Decimal('0.00')
        else:
            salary = Decimal('0.00')

        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.salary = salary
        user_profile.save()

        return self.get(request, *args, **kwargs)


# Adicionar despesa
class AddExpenseView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/add_expense.html'
    success_url = reverse_lazy('expense_list')

    def form_valid(self, form):
        expense = form.save(commit=False)
        expense.user = self.request.user
        expense.save()

        # Criação de despesas para cada mês adicional
        for i in range(expense.duration_months - 1):
            Expense.objects.create(
                expense_category=expense.expense_category,
                title=expense.title,
                amount=expense.amount,
                date=expense.date + timedelta(days=30 * (i + 1)),
                payment_method=expense.payment_method,
                observation=expense.observation,
                user=self.request.user,
                duration_months=1
            )

        return super().form_valid(form)


# Excluir despesa
class DeleteExpenseView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/delete_expense.html'
    success_url = reverse_lazy('expense_list')

    def get_object(self, queryset=None):
        expense_id = self.kwargs.get('expense_id')
        return get_object_or_404(Expense, id=expense_id)


# Excluir todas as despesas
class DeleteAllExpensesView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        Expense.objects.filter(user=request.user).delete()
        return redirect('expense_list')


# Confirmar exclusão de todas as despesas
class ConfirmDeleteExpensesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'expenses/confirm_delete.html')

    def post(self, request, *args, **kwargs):
        # Exclui todas as despesas do usuário logado
        Expense.objects.filter(user=request.user).delete()
        return redirect('expense_list')

# ------------------------------------------------------------

# Classe para retornar transações do usuário logado
class GetTransactionsView(LoginRequiredMixin, View):
    def get(self, request):
        # Filtra as transações para o usuário logado
        transactions = Transaction.objects.filter(user=request.user)
        return JsonResponse(list(transactions.values()), safe=False)

# Classe para adicionar transação associada ao usuário logado
class AddTransactionView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(request.body)
        
        # Salvar a transação no banco associada ao usuário logado
        transaction = Transaction.objects.create(
            type=data['type'],
            category=data['category'],
            amount=data['amount'],
            description=data['description'],
            date=data['date'],
            user=request.user
        )
        
        return JsonResponse({'message': 'Transação cadastrada com sucesso!'}, status=201)

# Classe para renderizar o gráfico
class ChartView(LoginRequiredMixin, View):
    def get(self, request):
        # Filtra as transações para o usuário logado
        transactions = Transaction.objects.filter(user=request.user)
        
        # Organiza as categorias e valores para o gráfico
        categories = [transaction.category for transaction in transactions]
        amounts = [transaction.amount for transaction in transactions]
        
        # Passa os dados para o template
        return render(request, "chart.html", {
            "categories": categories,
            "amounts": amounts,
        })

# Classe para deletar todas as transações do usuário logado
class DeleteUserTransactionsView(LoginRequiredMixin, View):
    def delete(self, request):
        # Apagar apenas as transações do usuário logado
        Transaction.objects.filter(user=request.user).delete()
        return JsonResponse({'message': 'Todas as suas transações foram apagadas com sucesso!'}, status=200)

# Classe para atualizar o gráfico com AJAX
class TransactionListView(View):
    def get(self, request, *args, **kwargs):
        transactions = Transaction.objects.filter(type="despesa").values('id', 'category', 'amount', 'description', 'date')
        return JsonResponse(list(transactions), safe=False)
