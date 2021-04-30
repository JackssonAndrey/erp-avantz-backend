from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from django.db import transaction

from users.authentication import SafeJWTAuthentication
from .models import Produtos
from .serializers import ProdutoSerializer
from instituicao.views import search_matriz

from detalhes_produto.models import ProdItens


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@csrf_exempt
def get_all(request):
    id_institution = request.user.instit_id
    id_matriz = search_matriz(id_institution)

    try:
        produtos = Produtos.objects.filter(id_matriz=id_matriz, ativo=2)
        produtos_serialized = ProdutoSerializer(produtos, many=True)
        return Response(produtos_serialized.data)
    except:
        raise exceptions.APIException(
            'Não foi possível pesquisar os produtos.')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@csrf_exempt
def find_products_by_name(request, name):
    id_institution = request.user.instit_id
    id_matriz = search_matriz(id_institution)
    estoque = []

    try:
        produtos = Produtos.objects.filter(
            id_matriz=id_matriz, descres__contains=name)
        produtos_serialized = ProdutoSerializer(produtos, many=True)

        for produto in produtos_serialized.data:
            dados = ProdItens.objects.filter(id_instit=id_institution, ativo=2, id_produtos=produto['id']).values(
                'id', 'id_produtos', 'est_frente', 'prvenda1', 'prvenda2', 'prvenda3', 'locavel').get()
            estoque.append(dados)

        return Response({'produtos': produtos_serialized.data, 'estoque': estoque})
    except:
        raise exceptions.APIException(
            'Não foi possível encontrar os produtos.', status.HTTP_500_INTERNAL_SERVER_ERROR)