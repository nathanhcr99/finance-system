from rest_framework import serializers
from .models import Conta, Transacao, CategoriaTransacao


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['id', 'user', 'balanco', 'data_criação']

class CategoriaTransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaTransacao
        fields = ['id', 'nome']

class TransacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacao
        fields = ['id', 'user', 'categoria', 'quantia', 'tipo', 'descrição', 'data']

