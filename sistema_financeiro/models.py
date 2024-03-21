from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Conta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balanco = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_criação = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conta de {self.user.username}"
    

class CategoriaTransacao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Transacao(models.Model):
    TRANSACTION_TYPES = (
        ('renda', 'Renda'),
        ('despesa', 'Despesa'),
        ('transferencia', 'Transferencia'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaTransacao, on_delete=models.SET_NULL, null=True, blank=True)
    quantia = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    descrição = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"O usuário {self.user.username} {self.get_type_display()} fez uma transação de {self.quantia}"