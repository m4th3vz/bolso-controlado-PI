from django.db import models
from django.contrib.auth.models import User

PAYMENT_CHOICES = (
    ('Dinheiro', 'Dinheiro'),
    ('Crédito', 'Crédito'),
    ('Débito', 'Débito'),
)

# Modelo para representar uma despesa
class Expense(models.Model):
    # Título da despesa
    title = models.CharField(max_length=100, verbose_name='Título')
    # Valor da despesa
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    # Data da despesa
    date = models.DateField(verbose_name='Data')
    # Usuário associado à despesa (chave estrangeira)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Forma de pagamento
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Forma de Pagamento')
    # Observação sobre a despesa
    observation = models.TextField(blank=True, null=True, verbose_name='Observação', max_length=60)

    class Meta:
        # Metadados para configurar o nome da tabela no banco de dados
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
        # Retorna uma representação em string da despesa (o título)
        return self.title
    
class UserProfile(models.Model):
    # Relacionamento um para um com o modelo de usuário padrão do Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campo para armazenar a renda mensal do usuário
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        # Retorna o nome de usuário associado ao perfil
        return self.user.username

