from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from api.permissions import IsAdminManagerOrSales
from django.db import IntegrityError

from api.models import Contract
from api.serializers import ContractSerializer, CreateContractSerializer, UpdateContractSerializer
from api.serializers import ContractDetailSerializer


# ----------------------------------------
#   Endpoints used to deal with contracts
# ----------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAdminManagerOrSales])
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
@permission_classes([IsAdminManagerOrSales])
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

    # Get detailed infos
    serializer = ContractDetailSerializer(contract)
    return Response(serializer.data)
