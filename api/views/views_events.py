from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminManagerOrSales

from api.models import Event, ManagementUser, SalesUser
from api.serializers import EventSerializer, CreateEventSerializer, UpdateEventSerializer, EventDetailSerializer


# ---------------------------
#   Events-related endpoints
# ---------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAdminManagerOrSales])
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

    # Is the request user the support team member associated with this event?
    event_support = event.Support_contact
    if event_support.support == request.user:
        user_is_support = True
    else:
        user_is_support = False

    # Or is it a manager/seller/admin?
    if not request.user.is_superuser\
       and not ManagementUser.objects.filter(manager=request.user)\
       and not SalesUser.objects.filter(seller=request.user):
        is_manager = False
    else:
        is_manager = True

    # If it's neither of them, exit
    if not is_manager and not user_is_support:
        return Response(status=status.HTTP_403_FORBIDDEN)

    # Delete: the support guy cannot delete an event
    if request.method == 'DELETE':
        if is_manager:
            event.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    # Get detailed infos - accessible to everyone
    elif request.method == 'GET':
        serializer = EventDetailSerializer(event)
        return Response(serializer.data)

    # Update: support cannot modify himself and the contract field -> remove fields
    if request.method == 'PUT':
        if user_is_support:
            request.data.pop('Contract')
            request.data.pop('Support_contact')

        serializer = UpdateEventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
