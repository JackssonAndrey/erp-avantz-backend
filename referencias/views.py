from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from datetime import datetime
from django.db import transaction

from users.authentication import SafeJWTAuthentication
from instituicao.models import Instit
from .models import Referencias
from .serializers import ReferenciasSerializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def index(request, id_person):
    try:
        references = Referencias.objects.filter(
            id_pessoa_cod_fk=id_person, situacao=1)
        references_serialized = ReferenciasSerializers(references, many=True)
        return Response(references_serialized.data)
    except:
        raise exceptions.APIException(
            'Não foi possivel pesquisar as referências deste registro.')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@csrf_exempt
@transaction.atomic
def store(request):
    references_array = request.data.get('personReferences')

    for reference in references_array:
        try:
            references_registered = Referencias(id_pessoa_cod_fk=reference['idPerson'],
                                                situacao=reference['referenceSituation'], tipo=reference['referenceType'], nome=reference['referenceName'], tel=reference['referencePhone'], endereco=reference['referenceAddress'], data_criacao=datetime.now())
            references_registered.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar os dados da referência')

    references = Referencias.objects.filter(
        id_pessoa_cod_fk=references_array[0]['idPerson'], situacao=1)
    references_serialized = ReferenciasSerializers(references, many=True)
    return Response(references_serialized.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@csrf_exempt
@transaction.atomic
def update(request):
    references_array = request.data.get('personReferences')

    for reference in references_array:
        try:
            personReference = Referencias.objects.get(
                pk=reference['idReference'])
            personReference.nome = reference['referenceName']
            personReference.tel = reference['referencePhone']
            personReference.endereco = reference['referenceAddress']
            personReference.tipo = reference['referenceType']
            personReference.save()
        except:
            raise exceptions.APIException(
                'Não foi possível atualizar o registro de referência')
    return Response({'detail': 'Todos os dados de referência foram atualizados'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@csrf_exempt
@transaction.atomic
def delete(request, id_reference):
    try:
        reference = Referencias.objects.get(pk=id_reference)
        reference.situacao = 0
        reference.save()
        return Response({'detail': 'Apagado com sucesso!'})
    except:
        raise exceptions.APIException('Não foi possível deletar o registro')
