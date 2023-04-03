from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import permission_classes
from api.permissions import IsAdminOrManager, IsAdminManagerOrSales

from api.models import ManagementUser, SalesUser, SupportUser
from api.serializers import CreateUserSerializer, UpdateUserSerializer
from api.serializers import SalesSerializer, SupportSerializer, ManagerSerializer


# --------------------------------------------------------
#   Endpoints reserved for superuser: manipulate managers
# --------------------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrManager])
def managers(request):
    """
    GET: See managers list
    POST: Add a new user in the management team
    """

    # Get full manager list
    if request.method == 'GET':
        manager_list = ManagementUser.objects.all()
        serializer = ManagerSerializer(manager_list, many=True)
        return Response(serializer.data)

    # Create a new manager
    elif request.method == 'POST':
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            new_user = serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Insert the newly created user in the dedicated table
        ManagementUser.objects.create(manager=new_user)

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrManager])
def managers_detail(request, manager_id):
    """
    GET: see manager infos
    PUT: update manager
    DELETE: ...
    """

    # Find manager or quit immediately
    try:
        manager = ManagementUser.objects.get(id=manager_id)
    except ManagementUser.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Get infos
    if request.method == 'GET':
        serializer = ManagerSerializer(manager)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update manager
    elif request.method == 'PUT':
        serializer = UpdateUserSerializer(manager.manager, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete manager (both user and entry in table) - a manager cannot delete himself, by convention
    elif request.method == 'DELETE':
        if request.user == manager.manager:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            manager.manager.delete()
            manager.delete()

    # Everything OK
    return Response(status=status.HTTP_200_OK)


# -------------------------------------------------
#   Endpoints used by managers to work with teams
# -------------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrManager])
def sales(request):
    """
    GET: See sellers list
    POST: Add a new user in the sales team
    """

    # Get full sales list
    if request.method == 'GET':
        sales_list = SalesUser.objects.all()
        serializer = SalesSerializer(sales_list, many=True)
        return Response(serializer.data)

    # Create a new seller
    elif request.method == 'POST':
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            new_user = serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Insert the newly created user in the dedicated table
        SalesUser.objects.create(seller=new_user)

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrManager])
def sales_detail(request, seller_id):
    """
    GET: see manager infos
    PUT: update manager
    DELETE: ...
    """

    # Find seller
    try:
        seller = SalesUser.objects.get(id=seller_id)
    except SalesUser.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Get infos
    if request.method == 'GET':
        serializer = SalesSerializer(seller)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update seller
    elif request.method == 'PUT':
        serializer = UpdateUserSerializer(seller.seller, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete seller (both user and entry in table)
    elif request.method == 'DELETE':
        seller.seller.delete()
        seller.delete()

    # Everything OK
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrManager])
def support(request):
    """
    GET: See support team list
    POST: Add a new user in the support team
    """

    # Get full support team list
    if request.method == 'GET':
        support_list = SupportUser.objects.all()
        serializer = SupportSerializer(support_list, many=True)
        return Response(serializer.data)

    # Create a new support team member
    elif request.method == 'POST':
        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            new_user = serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Insert the newly created user in the dedicated table
        SupportUser.objects.create(support=new_user)

        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrManager])
def support_detail(request, support_id):
    """
    GET: see manager infos
    PUT: update manager
    DELETE: ...
    """

    # Find seller
    try:
        support = SupportUser.objects.get(id=support_id)
    except SupportUser.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # Get infos
    if request.method == 'GET':
        serializer = SupportSerializer(support)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update seller
    elif request.method == 'PUT':
        serializer = UpdateUserSerializer(support.support, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete support (both user and entry in table)
    elif request.method == 'DELETE':
        support.support.delete()
        support.delete()

    # Everything OK
    return Response(status=status.HTTP_200_OK)
