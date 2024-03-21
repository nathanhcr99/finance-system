from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transacao,Conta,CategoriaTransacao
from rest_framework import status
from .serializers import TransacaoSerializer,ContaSerializer,CategoriaTransacaoSerializer
from rest_framework.permissions import IsAuthenticated


class TransactionList(APIView):

    """
    View para listar todas as transações do usuário.
    """
    def get(self, request):
        transacoes = Transacao.objects.filter(user=request.user)
        serializer = TransacaoSerializer(transacoes, many=True)
        return Response(serializer.data)
    
class AccountList(APIView):
    """
    View para listar todas as contas de usuários.
    """
       
    def get(self, request):
        contas = Conta.objects.filter(user=request.user)
        serializer = ContaSerializer(contas, many=True)
        return Response(serializer.data)

class AccountDetail(APIView):

    """
    View para detalhar uma conta específica do usuário.
    """
    def get(self, request, pk):
        conta = Conta.objects.get(pk=pk, user=request.usuario)
        serializer = ContaSerializer(conta)
        return Response(serializer.data)
    


class TransactionCategoryList(APIView):
    def get(self, request):
        categorias = CategoriaTransacao.objects.all()
        serializer = CategoriaTransacaoSerializer(categorias, many=True)
        return Response(serializer.data)
    


class TransactionDetail(APIView):
    """
    View para detalhar uma transação específica do usuário.
    """
    def get_object(self, pk):
        return get_object_or_404(Transacao, pk=pk, user=self.request.user)

    def get(self, request, pk):
        transacao = self.get_object(pk)
        serializer = TransacaoSerializer(transacao)
        return Response(serializer.data)

    def put(self, request, pk):
        transacao = self.get_object(pk)
        serializer = TransacaoSerializer(transacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        transacao = self.get_object(pk)
        transacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class AccountInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Recupera a conta do usuário logado
        user = request.user
        try:
            account = Conta.objects.get(user=user)
        except Conta.DoesNotExist:
            return Response({"message": "A conta do usuário não foi encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Serializa as informações da conta
        account_serializer = ContaSerializer(account)

        # Recupera as últimas transações da conta
        transactions = Transacao.objects.filter(account=account).order_by('-date')[:10]  # Obtém as últimas 10 transações
        transaction_serializer = TransacaoSerializer(transactions, many=True)

        # Constrói a resposta
        response_data = {
            "account_info": account_serializer.data,
            "transactions": transaction_serializer.data
        }

        return Response(response_data)
    

class Deposit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        user = request.user

        try:
            account = Conta.objects.get(user=user)
        except Conta.DoesNotExist:
            return Response({"message": "A conta do usuário não foi encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Realiza o depósito na conta do usuário
        account.balance += amount
        account.save()

        # Registra a transação de depósito
        transaction = Transacao.objects.create(account=account, amount=amount, type='deposit')

        serializer = TransacaoSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Withdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        user = request.user

        try:
            account = Conta.objects.get(user=user)
        except Conta.DoesNotExist:
            return Response({"message": "A conta do usuário não foi encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se há saldo suficiente para o saque
        if account.balance < amount:
            return Response({"message": "Saldo insuficiente para o saque."}, status=status.HTTP_400_BAD_REQUEST)

        # Realiza o saque na conta do usuário
        account.balance -= amount
        account.save()

        # Registra a transação de saque
        transaction = Transacao.objects.create(account=account, amount=amount, type='withdrawal')

        serializer = TransacaoSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class Transfer(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        to_account_id = request.data.get('to_account_id')
        from_user = request.user

        try:
            from_account = Conta.objects.get(user=from_user)
            to_account = Conta.objects.get(id=to_account_id)
        except Conta.DoesNotExist:
            return Response({"message": "A conta do usuário não foi encontrada."}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se há saldo suficiente para a transferência
        if from_account.balance < amount:
            return Response({"message": "Saldo insuficiente para a transferência."}, status=status.HTTP_400_BAD_REQUEST)

        # Realiza a transferência entre contas
        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()

        # Registra a transação de transferência
        transaction = Transacao.objects.create(account=from_account, amount=-amount, type='transfer', description=f"Transferência para conta {to_account_id}")

        serializer = TransacaoSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    



class TransactionHistory(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        transactions = Transacao.objects.filter(account__user=user)

        # Filtrar por data (se fornecido)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date and end_date:
            transactions = transactions.filter(date__range=[start_date, end_date])

        # Filtrar por tipo de operação (se fornecido)
        transaction_type = request.query_params.get('type', None)
        if transaction_type:
            transactions = transactions.filter(type=transaction_type)

        serializer = TransacaoSerializer(transactions, many=True)
        return Response(serializer.data)
    

