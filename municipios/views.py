from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from django.db import transaction
from django.db.models import Count

from users.authentication import SafeJWTAuthentication

from .models import Municipios
from .serializers import MunicipiosSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def index(request):
    try:
        counties = Municipios.objects.all()
        counties_serialized = MunicipiosSerializer(counties, many=True)
        return Response(counties_serialized.data)
    except:
        raise exceptions.APIException(
            'Não foi possível pesquisar os municípios', code=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def select_ufs(request):
    try:
        ufs = []
        counties = Municipios.objects.order_by(
            'uf_sigla').values('uf_sigla', 'id_municipios').distinct()

        i = 0
        for c in counties:
            if len(ufs) == 0:
                ufs.append(
                    dict(id_municipios=c['id_municipios'], uf_sigla=c['uf_sigla']))

            while ufs[i]['uf_sigla'] != c['uf_sigla']:
                ufs.append(
                    dict(id_municipios=c['id_municipios'], uf_sigla=c['uf_sigla']))
                i += 1

        return Response(ufs)
    except:
        raise exceptions.APIException(
            'Não foi possível pesquisar os municípios', code=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def select_cities(request, uf_id):
    try:
        countie = Municipios.objects.filter(
            id_municipios=uf_id).values('uf_sigla').first()

        cities = Municipios.objects.filter(uf_sigla=countie['uf_sigla'])
        cities_serialized = MunicipiosSerializer(cities, many=True)

        return Response(cities_serialized.data)
    except:
        raise exceptions.APIException(
            'Não foi possível retornar os dados dos Municípios.')
