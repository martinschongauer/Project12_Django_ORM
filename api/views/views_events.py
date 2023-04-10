from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from api.permissions import SupportReadOnly
from rest_framework.permissions import IsAuthenticated

from api.models import Event, ManagementUser
from api.serializers import EventSerializer, CreateEventSerializer, UpdateEventSerializer, EventDetailSerializer


# ---------------------------
#   Events-related endpoints
# ---------------------------

def write_access_to_event(event, request):
    """
    In order to modify existing event infos, more subtle checks are needed
    param event: the event to be accessed
    param request: the whole request to be examined
    return value: True if access is granted
    """
    user = request.user

    # Easy case: is user a manager/admin?
    if user.is_superuser or ManagementUser.objects.filter(manager=user):
        return True

    # Sales team member? Then we must be associated with this contract and/or client
    contract = event.Contract
    client = contract.Client
    if contract.Sales_contact.seller == user or client.Sales_contact.seller == user:
        return True

    # Is the request user the support team member associated with this event?
    event_support = event.Support_contact
    if event_support.support == request.user:
        # Support Team members cannot delete an event
        if request.method == 'DELETE':
            return False
        # But thy can modify it, except two sensitive fields
        else:
            if 'Contract' in request.data:
                request.data.pop('Contract')
            if 'Support_contact' in request.data:
                request.data.pop('Support_contact')
            return True

    # We did not fall into any allowed category
    return False


@api_view(['GET', 'POST'])
@permission_classes([SupportReadOnly])
def events(request):
    """
    GET: See all events (summary)
    """

    # Get contracts list
    if request.method == 'GET':
        events_list = Event.objects.filter()
        serializer = EventSerializer(events_list, many=True)
        return Response(serializer.data)

    # POST = Create a new event
    elif request.method == 'POST':
        serializer = CreateEventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

        return Response(status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_detail(request, event_id):
    """
    GET: See detailed information about an event
    PUT: Modify an event's infos
    DELETE: Deletes an event
    """

    # Find event
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Get detailed infos - accessible to everyone
    if request.method == 'GET':
        serializer = EventDetailSerializer(event)
        return Response(serializer.data)

    # To get further, we need particular authorizations
    if not write_access_to_event(event, request):
        return Response(status=status.HTTP_403_FORBIDDEN)

    # Delete: the support guy cannot delete an event
    if request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_200_OK)

    # Update: support cannot modify himself and the contract field -> remove fields
    if request.method == 'PUT':
        serializer = UpdateEventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
