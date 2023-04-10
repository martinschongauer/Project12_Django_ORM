from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from api.permissions import SupportReadOnly

from api.models import Contract, SalesUser
from api.serializers import ContractSerializer, CreateContractSerializer, UpdateContractSerializer
from api.serializers import ContractDetailSerializer


# ----------------------------------------
#   Endpoints used to deal with contracts
# ----------------------------------------

def write_access_to_contract(contract, user):
    """
    In order to modify existing contract infos, more subtle checks are needed
    param contract: the contract to be accessed
    param user: the logged user
    return value: True if access is granted
    """
    # Sales team member? Then we must be associated with this contract and/or client
    if SalesUser.objects.filter(seller=user):
        client = contract.Client
        if contract.Sales_contact.seller == user or client.Sales_contact.seller == user:
            return True
        else:
            return False

    # Admin or manager: OK
    return True


@api_view(['GET', 'POST'])
@permission_classes([SupportReadOnly])
def contracts(request):
    """
    GET: See all contracts (summary)
    """

    # Get contracts list
    if request.method == 'GET':
        contracts_list = Contract.objects.filter()
        serializer = ContractSerializer(contracts_list, many=True)
        return Response(serializer.data)

    # POST = Create a new contract
    elif request.method == 'POST':
        serializer = CreateContractSerializer(data=request.data)
        # try:
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
        # except IntegrityError:
        #    return Response(status.HTTP_400_BAD_REQUEST)

        return Response(status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([SupportReadOnly])
def contract_detail(request, contract_id):
    """
    GET: See detailed information about a client
    PUT: Modify a client's infos
    DELETE: Deletes a client (it will be cascaded to its contracts/events)
    """

    # Find contract
    try:
        contract = Contract.objects.get(id=contract_id)
    except Contract.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Get detailed infos
    if request.method == 'GET':
        serializer = ContractDetailSerializer(contract)
        return Response(serializer.data)

    # PUT and DELETE require additional verifications
    if not write_access_to_contract(contract, request.user):
        return Response(status=status.HTTP_403_FORBIDDEN)

    # Update
    if request.method == 'PUT':
        serializer = UpdateContractSerializer(contract, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Delete
    elif request.method == 'DELETE':
        contract.delete()
        return Response(status=status.HTTP_200_OK)
