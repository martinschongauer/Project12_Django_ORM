from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from api.permissions import SupportReadOnly

from api.models import Client, SalesUser
from api.serializers import ClientSerializer, CreateClientSerializer, UpdateClientSerializer, ClientDetailSerializer


# ---------------------------------------
#   Endpoints used to deal with Clients
# ---------------------------------------

def write_access_to_client(client, user):
    """
    In order to modify existing client infos, more subtle checks are needed
    param client: the client to be accessed
    param user: the logged user
    return value: True if access is granted
    """
    # Sales team member? Then we must be associated with this client
    if SalesUser.objects.filter(seller=user):
        if client.Sales_contact.seller == user:
            return True
        else:
            return False

    # Admin or manager: OK
    return True


@api_view(['GET', 'POST'])
@permission_classes([SupportReadOnly])
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
@permission_classes([SupportReadOnly])
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

    # Read detailed infos
    if request.method == 'GET':
        serializer = ClientDetailSerializer(client)
        return Response(serializer.data)

    # PUT and DELETE require additional verifications
    if not write_access_to_client(client, request.user):
        return Response(status=status.HTTP_403_FORBIDDEN)

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
