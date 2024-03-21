from django.contrib import admin
from .models import Conta, Transacao,CategoriaTransacao

# Register your models here.
admin.site.register(Conta)
admin.site.register(Transacao)
admin.site.register(CategoriaTransacao)