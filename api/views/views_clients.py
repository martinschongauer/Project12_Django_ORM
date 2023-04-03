from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from api.permissions import IsAdminManagerOrSales

from api.models import Client
from api.serializers import ClientSerializer, CreateClientSerializer, UpdateClientSerializer, ClientDetailSerializer


# ---------------------------------------
#   Endpoints used to deal with Clients
# ---------------------------------------


@api_view(['GET', 'POST'])
@permission_classes([IsAdminManagerOrSales])
def clients(request):
    """
    GET: See a list of clients
    POST: Add a new client to the list
    parameter known = False -> no contracts signed from now / True -> already a "real" client
    """

    # Get full list
    if request.method == 'GET':
        known_client = request.GET.get('known', '')
        clients_list = Client.objects.filter(Client_known=known_client)
        serializer = ClientSerializer(clients_list, many=True)
        return Response(serializer.data)

    # Create a new client
    elif request.method == 'POST':
        serializer = CreateClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminManagerOrSales])
def client_detail(request, client_id):
    """
    GET: See detailed information about a client
    PUT: Modify a client's infos
    DELETE: Deletes a client (it will be cascaded to its contracts/events)
    """

    # Find client before treating any operation
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Update
    if request.method == 'PUT':
        serializer = UpdateClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Delete
    elif request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_200_OK)

    # By default, get detailed infos
    serializer = ClientDetailSerializer(client)
    return Response(serializer.data)
