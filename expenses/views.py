from .models import Expense, UserProfile
from .forms import ExpenseForm, UserRegistrationForm
from decimal import Decimal, InvalidOperation
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

# Lista de despesas
@login_required
def expense_list(request):
    if request.method == 'POST':
        salary = request.POST.get('salary')

        # Verifica se o campo de renda mensal está vazio ou não é um número
        if not salary:
            salary = Decimal('0.00')  # Define a renda mensal como 0.00 se estiver vazio
        else:
            try:
                salary = Decimal(salary)  # Tenta converter o valor da renda mensal para Decimal
            except (ValueError, InvalidOperation):
                # Se ocorrer um erro de conversão, define o valor como zero
                salary = Decimal('0.00')

        # Salva a renda mensal associada ao usuário logado
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.salary = salary
        user_profile.save()

    expenses = Expense.objects.filter(user=request.user)
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    # Arredonda o total de despesas para 2 casas decimais
    total_expenses = round(total_expenses, 2)
    salary = UserProfile.objects.get(user=request.user).salary if UserProfile.objects.filter(user=request.user).exists() else None
    
    # Calcula a diferença entre a renda mensal e o total das despesas
    difference = salary - total_expenses if salary is not None else None

    return render(request, 'expenses/expense_list.html', {'expenses': expenses, 'total_expenses': total_expenses, 'salary': salary, 'difference': difference})

# Adicionar despesa
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            # Salva a despesa associada ao usuário logado
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})

# Excluir despesa
@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/delete_expense.html', {'expense': expense})

# Excluir todas as despesas
@login_required
def delete_all_expenses(request):
    if request.method == 'POST':
        Expense.objects.all().delete()
        return redirect('expense_list')
    return redirect('confirm_delete_expenses')

# Confirmar exclusão de todas as despesas
@login_required
def confirm_delete_expenses(request):
    return render(request, 'expenses/confirm_delete.html')

# Página da calculadora
@login_required
def calculator(request):
    return render(request, 'calculator.html')

# Personalização da página de login
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('welcome')

# Página de registro de usuário
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Página de boas-vindas
@login_required
def welcome(request):
    return render(request, 'welcome.html')
