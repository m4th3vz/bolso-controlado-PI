# expenses/models.py
from django.db import models
from django.contrib.auth.models import User

# Defina suas opções de categoria
CATEGORY_CHOICES = (
    ('Casa', 'Casa'),
    ('Contas', 'Contas'),
    ('Alimentação', 'Alimentação'),
    ('Saúde', 'Saúde'),
    ('Educação', 'Educação'),
    ('Lazer', 'Lazer'),
    ('Compras', 'Compras'),
    ('Viagem', 'Viagem'),
    ('Serviços', 'Serviços'),
    ('Vestuário', 'Vestuário'),
    ('Impostos', 'Impostos'),
    ('Transporte', 'Transporte'),
    ('Investimentos', 'Investimentos'),
    ('Outros', 'Outros'),
)

# Defina suas opções de forma de pagamento
PAYMENT_CHOICES = (
    ('Dinheiro', 'Dinheiro'),
    ('Crédito', 'Crédito'),
    ('Débito', 'Débito'),
    ('Pix', 'Pix'),
    ('Boleto', 'Boleto'),
    ('Voucher', 'Voucher'),
    ('Crediário', 'Crediário'),
    ('Transferência', 'Transferência'),
    ('Cartão de loja', 'Cartão de loja'),
)

# Modelo para representar uma despesa
class Expense(models.Model):
    expense_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='Categoria', default='categoria1')
    title = models.CharField(max_length=30, verbose_name='Título')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    date = models.DateField(verbose_name='Data')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    payment_method = models.CharField(blank=True, max_length=20, choices=PAYMENT_CHOICES, verbose_name='Forma de Pagamento (Opcional)', default='Dinheiro')
    observation = models.TextField(blank=True, verbose_name='Observação', max_length=60)
    duration_months = models.IntegerField(verbose_name='Duração em Meses', default=1)

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
        return self.title


# Modelo para representar um usuário
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username


# Dashboard Financeiro
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
    ]

    CATEGORY_CHOICES = [
        ('essential', 'Essential Expenses'),
        ('fixed', 'Fixed Expenses'),
        ('pharmacy', 'Pharmacy'),
        ('transport', 'Transport'),
        ('maintenance', 'Maintenance'),
        ('market', 'Market'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
    ]

    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type} - {self.category} - {self.amount} - {self.user.username}"
    