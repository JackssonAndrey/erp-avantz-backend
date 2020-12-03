from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from django.db import transaction

from users.authentication import SafeJWTAuthentication
from .serializers import PescodSerializer
from .models import Pescod
from pessoa_fisica.models import Pesfis
from pessoa_fisica.serializers import PessoaFisicaSerializers
from pessoa_juridica.models import Pesjur
from pessoa_juridica.serializers import PessoaJuridicaSerializer
from enderecos.models import Enderecos
from enderecos.serializers import EnderecosSerializers
from telefones.models import Telefones
from telefones.serializers import TelefoneSerializers
from emails.models import Mails
from emails.serializers import EmailSerializers
from referencias.models import Referencias
from referencias.serializers import ReferenciasSerializers
from ref_bancarias.models import Refbanco
from ref_bancarias.serializers import RefBancoSerializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def index(request):
    id_institution = request.user.instit_id
    try:
        persons = Pescod.objects.filter(
            id_instituicao_fk=id_institution, sit=2)
        persons_serialized = PescodSerializer(persons, many=True)
        return Response(persons_serialized.data)
    except:
        raise exceptions.APIException


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def find_physical_persons(request):
    id_institution = request.user.instit_id
    try:
        persons = Pescod.objects.filter(
            id_instituicao_fk=id_institution, sit=2, tipo=1)
        persons_serialized = PescodSerializer(persons, many=True)
        return Response(persons_serialized.data)
    except:
        raise exceptions.APIException


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def find_legal_persons(request):
    id_institution = request.user.instit_id
    try:
        persons = Pescod.objects.filter(
            id_instituicao_fk=id_institution, sit=2, tipo=2)
        persons_serialized = PescodSerializer(persons, many=True)
        return Response(persons_serialized.data)
    except:
        raise exceptions.APIException


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
@transaction.atomic
def store_person_physical(request):
    id_institution = request.user.instit_id
    cpf = request.data.get('personCPF')
    """  
    FIND CPF ON DATABASE. IF EXIST, NO REGISTER AND RETURN
    """
    person = Pescod.objects.filter(
        id_instituicao_fk=id_institution, cpfcnpj=cpf, sit=2)
    if person:
        return Response({'detail': 'Já existe um registro ativo com este CPF. Por favor revise os dados.'}, status=status.HTTP_400_BAD_REQUEST)

    """  
    REGISTER PESCOD
    """
    provider = request.data.get('personIsProvider')
    name = request.data.get('personName')
    person_photo = request.data.get('personPhoto')
    person_limit = request.data.get('personLimit')
    person_balance = request.data.get('personBalance')

    try:
        person = Pescod(id_instituicao_fk=id_institution, tipo=1, sit=1, forn=provider, cpfcnpj=cpf,
                        nomeorrazaosocial=name, foto=person_photo, img_bites=0, limite=person_limit, saldo=person_balance, data_criacao=timezone.now())
        person.save()
    except:
        raise exceptions.APIException(
            'Não foi possível cadastrar o registro da pessoa. Verifique os dados inseridos.')

    """  
    REGISTER PHYSICAL PERSON
    """
    person_registred_id = person.id_pessoa_cod
    identity = request.data.get('personIdentity')
    issuer_identity = request.data.get('issuerIdentity')
    id_municipality = request.data.get('personMunicipality')
    id_uf = request.data.get('personUF')
    date_of_birth = request.data.get('personBirth')
    treatment = request.data.get('personTreatment')
    nickname = request.data.get('personNickname')
    sex = request.data.get('personSex')
    father = request.data.get('personFather')
    mother = request.data.get('personMother')
    profession = request.data.get('personProfession')
    ctps = request.data.get('ctps')
    salary = request.data.get('personSalary')
    company = request.data.get('personCompany')
    company_responsible = request.data.get('companyResponsible')
    company_cnpj = request.data.get('companyCnpj')
    state_registration = request.data.get('stateRegistrationCompany')
    municipal_registration = request.data.get('municipalRegistrationCompany')
    company_adress = request.data.get('companyAdress')
    other_income = request.data.get('otherIncome')
    income_value = request.data.get('incomeValue')
    irpf = request.data.get('irpf')
    marital_status = request.data.get('maritalStatus')
    dependents = request.data.get('personDependents')
    pension = request.data.get('pension')
    spouse = request.data.get('spouse')
    spouse_cpf = request.data.get('spouseCpf')
    spouse_profession = request.data.get('spouseProfession')
    spouse_company = request.data.get('spouseCompany')
    spouse_income = request.data.get('spouseIncome')
    spouse_phone = request.data.get('spousePhone')
    spouse_mail = request.data.get('spouseMail')

    person_physical = Pesfis(id_pessoa_cod_fk=person_registred_id, identidade=identity, emissor_identidade=issuer_identity, id_municipio_fk=id_municipality,
                             id_uf_municipio_fk=id_uf, data_de_nascimento=date_of_birth, tratam=treatment, apelido=nickname, sexo=sex, pai=father, mae=mother,
                             profissao=profession, ctps=ctps, salario=salary, empresa=company, resp=company_responsible, cnpj=company_cnpj, iest=state_registration,
                             imun=municipal_registration, emprend=company_adress, orendas=other_income, vrendas=income_value, irpf=irpf, estcivil=marital_status,
                             depend=dependents, pensao=pension, conjuge=spouse, cpfconj=spouse_cpf, profconj=spouse_profession, emprconj=spouse_company,
                             rendaconj=spouse_income, telconj=spouse_phone, mailconj=spouse_mail, data_criacao=timezone.now())

    try:
        person_physical.save()
    except:
        raise exceptions.APIException(
            'Não foi possível cadastrar os dados de pessoa física')

    """ 
    REGISTER ADRESS
    """
    adresses_array = request.data.get('adresses')
    for adress in adresses_array:
        try:
            adress_registred = Enderecos(situacao=1, origem=1, id_pessoa_cod_fk=person_registred_id, endtip=1, rua=adress['street'],
                                         numero=adress['numberHouse'], complemento=adress['complement'], bairro=adress['neighborhood'],
                                         cep=adress['zipCode'], cidade=adress['city'], estado_endereco=adress['stateAdress'], data_criacao=timezone.now())
            adress_registred.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar todos os dados de endereço')

    """  
    REGISTER PHONE
    """
    phones_array = request.data.get('phones')
    for phone in phones_array:
        try:
            phone_registered = Telefones(id_pessoa_cod_fk=person_registred_id,
                                         situacao=1, tel=phone['phoneNumber'], data_criacao=timezone.now())
            phone_registered.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar os dados de contato')

    """ 
    REGISTER MAIL    
    """
    mails_array = request.data.get('mails')
    for mail in mails_array:
        try:
            mail_registered = Mails(
                id_pessoa_cod_fk=person_registred_id, situacao=1, email=mail['userMail'], data_criacao=timezone.now())
            mail_registered.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar os dados de email')

    """  
    REGISTER REFERENCES
    """
    references_array = request.data.get('personReferences')
    for reference in references_array:
        try:
            references_registered = Referencias(id_pessoa_cod_fk=person_registred_id,
                                                situacao=1, tipo=reference['referenceType'], nome=reference['referenceName'],
                                                tel=reference['referencePhone'], endereco=reference['referenceAdress'], data_criacao=timezone.now())
            references_registered.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar os dados da referência')

    """  
    REGISTER BANK
    """
    banking_references_array = request.data.get('bankingReferences')
    for banking_reference in banking_references_array:
        try:
            banking_reference_registred = Refbanco(id_pessoa_cod_fk=person_registred_id, id_bancos_fk=banking_reference['idBanking'], situacao=1,
                                                   agencia=banking_reference['agency'], conta=banking_reference['account'],
                                                   abertura=banking_reference['opening'], tipo=banking_reference['type'], data_criacao=timezone.now())
            banking_reference_registred.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar os dados de refenrências bancárias')

    return Response({'detail': 'Cadastro feito com sucesso'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def delete(request, id_person):
    try:
        person = Pescod.objects.get(pk=id_person)
        person.sit = 0
        person.save()
        return Response({'detail': 'Apagado com sucesso!'})
    except:
        raise exceptions.APIException('Não foi possível deletar o registro')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def details_physical_person(request, id_person):
    # LIST OF THE POSSIBLE SEARCH ERRORS IN THE DATA OF THE PERSON SEARCHED
    details = []

    try:
        person = Pescod.objects.get(pk=id_person)
        person_serialized = PescodSerializer(person)
    except:
        raise exceptions.APIException(
            'Não foi possível pesquisar os dados do registro.')

    # FIND PHYSICAL PERSON DATA
    person_physical = Pesfis.objects.get(id_pessoa_cod_fk=id_person)
    if not person_physical:
        details.append(
            'Não foi possível encontrar os dados deste registro.')
    person_physical_serialized = PessoaFisicaSerializers(
        person_physical)

    # FIND ADRESS DATA THIS PERSON
    person_adress = Enderecos.objects.filter(id_pessoa_cod_fk=id_person)
    if not person_adress:
        details.append(
            'Não foi possível encontrar os dados de endereço deste registro.')
    person_adress_serialized = EnderecosSerializers(
        person_adress, many=True)

    # FIND PHONE DATA THIS PERSON
    person_phone = Telefones.objects.filter(id_pessoa_cod_fk=id_person)
    if not person_phone:
        details.append(
            'Não foi possível encontrar os dados de contato deste registro.')
    person_phone_serialized = TelefoneSerializers(person_phone, many=True)

    # FIND MAIL DATA THIS PERSON
    person_mail = Mails.objects.filter(id_pessoa_cod_fk=id_person)
    if not person_physical:
        details.append(
            'Não foi possível encontrar os dados de e-mail deste registro.')
    person_mail_serialized = EmailSerializers(person_mail, many=True)

    # FIND REFERENCES DATA THIS PERSON
    person_references = Referencias.objects.filter(
        id_pessoa_cod_fk=id_person)
    if not person_references:
        details.append(
            'Não foi possível encontrar os dados de referência deste registro.')
    person_references_serialized = ReferenciasSerializers(
        person_references, many=True)

    # FIND BANKING REFERENCES DATA THIS PERSON
    banking_references = Refbanco.objects.filter(
        id_pessoa_cod_fk=id_person)
    if not banking_references:
        details.append(
            'Não foi possível encontrar os dados bancários deste registro.')
    banking_references_serialized = RefBancoSerializers(
        banking_references, many=True)

    return Response({
        'person': person_serialized.data,
        'personPhysical': person_physical_serialized.data,
        'personAdress': person_adress_serialized.data,
        'personPhone': person_phone_serialized.data,
        'personMail': person_mail_serialized.data,
        'personReferences': person_references_serialized.data,
        'bankingReferences': banking_references_serialized.data,
        'details': details
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
@transaction.atomic
def store_legal_person(request):
    id_institution = request.user.instit_id
    cnpj = request.data.get('personCNPJ')
    """  
    FIND CPF ON DATABASE. IF EXIST, NO REGISTER AND RETURN
    """
    person = Pescod.objects.filter(
        id_instituicao_fk=id_institution, cpfcnpj=cnpj, sit=2)
    if person:
        return Response({'detail': 'Já existe um registro ativo com este CNPJ. Por favor revise os dados.'}, status=status.HTTP_400_BAD_REQUEST)

    """  
    REGISTER PESCOD
    """
    provider = request.data.get('personIsProvider')
    company_name = request.data.get('companyName')
    person_photo = request.data.get('personPhoto')
    person_limit = request.data.get('personLimit')
    person_balance = request.data.get('personBalance')

    try:
        person = Pescod(id_instituicao_fk=id_institution, tipo=2, sit=2, forn=provider, cpfcnpj=cnpj,
                        nomeorrazaosocial=company_name, foto=person_photo, img_bites=0, limite=person_limit, saldo=person_balance, data_criacao=timezone.now())
        person.save()
    except:
        raise exceptions.APIException(
            'Não foi possível cadastrar o registro da pessoa. Verifique os dados inseridos.')

    """  
    REGISTER LEGAL PERSON
    """
    person_registred_id = person.id_pessoa_cod
    fantasy_name = request.data.get('fantasyName')
    branch = request.data.get('branch')
    company_type = request.data.get('companyType')
    share_capital = request.data.get('shareCapital')
    revenues = request.data.get('revenues')
    taxation = request.data.get('taxation')
    contact = request.data.get('contact')
    open_date = request.data.get('openDate')
    state_registration = request.data.get('stateRegistrationCompany')
    municipal_registration = request.data.get('municipalRegistrationCompany')

    try:
        legal_person = Pesjur(id_pessoa_cod_fk=person_registred_id, fantasia=fantasy_name, ramo=branch, inscricao_estadual=state_registration,
                              inscricao_municipal=municipal_registration, tipo_empresa=company_type, capsocial=share_capital, faturamento=revenues,
                              tribut=taxation, contato=contact, data_abertura=open_date, data_criacao=timezone.now())
        legal_person.save()
    except:
        raise exceptions.APIException(
            'Não foi possível cadastrar os dados de pessoa jurídica')

    """ 
    REGISTER ADRESS
    """
    adresses_array = request.data.get('adresses')
    for adress in adresses_array:
        try:
            adress_registred = Enderecos(situacao=1, origem=1, id_pessoa_cod_fk=person_registred_id, endtip=1, rua=adress['street'],
                                         numero=adress['numberHouse'], complemento=adress['complement'], bairro=adress['neighborhood'],
                                         cep=adress['zipCode'], cidade=adress['city'], estado_endereco=adress['stateAdress'], data_criacao=timezone.now())
            adress_registred.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar todos os dados de endereço')

    """  
    REGISTER PHONE
    """
    phones_array = request.data.get('phones')
    for phone in phones_array:
        try:
            phone_registered = Telefones(id_pessoa_cod_fk=person_registred_id,
                                         situacao=1, tel=phone['phoneNumber'], data_criacao=timezone.now())
            phone_registered.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar os dados de contato')

    """ 
    REGISTER MAIL    
    """
    mails_array = request.data.get('mails')
    for mail in mails_array:
        try:
            mail_registered = Mails(
                id_pessoa_cod_fk=person_registred_id, situacao=1, email=mail['userMail'], data_criacao=timezone.now())
            mail_registered.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar os dados de email')

    """  
    REGISTER REFERENCES
    """
    references_array = request.data.get('personReferences')
    for reference in references_array:
        try:
            references_registered = Referencias(id_pessoa_cod_fk=person_registred_id,
                                                situacao=1, tipo=reference['referenceType'], nome=reference['referenceName'],
                                                tel=reference['referencePhone'], endereco=reference['referenceAdress'], data_criacao=timezone.now())
            references_registered.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar os dados da referência')

    """  
    REGISTER BANK
    """
    banking_references_array = request.data.get('bankingReferences')
    for banking_reference in banking_references_array:
        try:
            banking_reference_registred = Refbanco(id_pessoa_cod_fk=person_registred_id, id_bancos_fk=banking_reference['idBanking'], situacao=1,
                                                   agencia=banking_reference['agency'], conta=banking_reference['account'],
                                                   abertura=banking_reference['opening'], tipo=banking_reference['type'], data_criacao=timezone.now())
            banking_reference_registred.save()
        except:
            raise exceptions.APIException(
                'Não foi possível salvar os dados de refenrências bancárias')

    return Response({'detail': 'Cadastro feito com sucesso'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([SafeJWTAuthentication])
@ensure_csrf_cookie
def details_legal_person(request, id_person):
    # LIST OF THE POSSIBLE SEARCH ERRORS IN THE DATA OF THE PERSON SEARCHED
    details = []

    # FIND DATA OF THE TABLE PESCOD
    try:
        person = Pescod.objects.get(pk=id_person)
        person_serialized = PescodSerializer(person)
    except:
        raise exceptions.APIException(
            'Não foi possível pesquisar os dados do registro.')

    # FIND LEGAL PERSON DATA
    legal_person = Pesjur.objects.get(id_pessoa_cod_fk=id_person)
    if not legal_person:
        details.append(
            'Não foi possível encontrar os dados deste registro.')
    legal_person_serialized = PessoaJuridicaSerializer(
        legal_person)

    # FIND ADRESS DATA THIS PERSON
    person_adress = Enderecos.objects.filter(id_pessoa_cod_fk=id_person)
    if not person_adress:
        details.append(
            'Não foi possível encontrar os dados de endereço deste registro.')
    person_adress_serialized = EnderecosSerializers(
        person_adress, many=True)

    # FIND PHONE DATA THIS PERSON
    person_phone = Telefones.objects.filter(id_pessoa_cod_fk=id_person)
    if not person_phone:
        details.append(
            'Não foi possível encontrar os dados de contato deste registro.')
    person_phone_serialized = TelefoneSerializers(person_phone, many=True)

    # FIND MAIL DATA THIS PERSON
    person_mail = Mails.objects.filter(id_pessoa_cod_fk=id_person)
    if not person_mail:
        details.append(
            'Não foi possível encontrar os dados de e-mail deste registro.')
    person_mail_serialized = EmailSerializers(person_mail, many=True)

    # FIND REFERENCES DATA THIS PERSON
    person_references = Referencias.objects.filter(
        id_pessoa_cod_fk=id_person)
    if not person_references:
        details.append(
            'Não foi possível encontrar os dados de referência deste registro.')
    person_references_serialized = ReferenciasSerializers(
        person_references, many=True)

    # FIND BANKING REFERENCES DATA THIS PERSON
    banking_references = Refbanco.objects.filter(
        id_pessoa_cod_fk=id_person)
    if not banking_references:
        details.append(
            'Não foi possível encontrar os dados bancários deste registro.')
    banking_references_serialized = RefBancoSerializers(
        banking_references, many=True)

    return Response({
        'person': person_serialized.data,
        'personPhysical': legal_person_serialized.data,
        'personAdress': person_adress_serialized.data,
        'personPhone': person_phone_serialized.data,
        'personMail': person_mail_serialized.data,
        'personReferences': person_references_serialized.data,
        'bankingReferences': banking_references_serialized.data,
        'details': details
    })
