from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import User, Client, Contract, Event, ManagementUser, SalesUser, SupportUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'id']


class CreateUserSerializer(serializers.ModelSerializer):

    # class Meta:
    #    model = User
    #    fields = ['first_name', 'last_name', 'email', 'username', 'password']
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ManagerSerializer(serializers.ModelSerializer):

    manager = serializers.SerializerMethodField()

    class Meta:
        model = ManagementUser
        fields = ['id', 'manager']

    def get_manager(self, instance):
        queryset = instance.manager
        serializer = UserSerializer(queryset)
        return serializer.data


class SalesSerializer(serializers.ModelSerializer):

    seller = serializers.SerializerMethodField()

    class Meta:
        model = SalesUser
        fields = ['id', 'seller']

    def get_seller(self, instance):
        queryset = instance.seller
        serializer = UserSerializer(queryset)
        return serializer.data


class SupportSerializer(serializers.ModelSerializer):

    support = serializers.SerializerMethodField()

    class Meta:
        model = SupportUser
        fields = ['id', 'support']

    def get_support(self, instance):
        queryset = instance.support
        serializer = UserSerializer(queryset)
        return serializer.data


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['First_name', 'Last_name', 'Company_name', 'Email', 'id']


class CreateClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['First_name', 'Last_name', 'Company_name', 'Email',
                  'Phone', 'Mobile', 'Client_known', 'Sales_contact']
        validators = [
            UniqueTogetherValidator(
                queryset=Client.objects.all(),
                fields=['Email', 'Company_name']
            )
        ]


class UpdateClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ['First_name', 'Last_name', 'Company_name', 'Email',
                  'Phone', 'Mobile', 'Client_known', 'Sales_contact']
        validators = [
            UniqueTogetherValidator(
                queryset=Client.objects.all(),
                fields=['Email', 'Company_name']
            )
        ]


class ClientDetailSerializer(serializers.ModelSerializer):

    sales_contact = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['First_name', 'Last_name', 'Company_name', 'Email',
                  'Phone', 'Mobile', 'Client_known', 'id', 'sales_contact']

    def get_sales_contact(self, instance):
        queryset = instance.Sales_contact
        serializer = SalesSerializer(queryset)
        return serializer.data


class ContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['Amount', 'Payment_Due', 'Title', 'id']


class CreateContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['Amount', 'Payment_Due', 'Title', 'Status', 'Sales_contact', 'Client']
        validators = [
            UniqueTogetherValidator(
                queryset=Contract.objects.all(),
                fields=['Title', 'Client']
            )
        ]


class UpdateContractSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['Amount', 'Payment_Due', 'Title', 'Status', 'Sales_contact', 'Client']
        validators = [
            UniqueTogetherValidator(
                queryset=Contract.objects.all(),
                fields=['Title', 'Client']
            )
        ]


class ContractDetailSerializer(serializers.ModelSerializer):

    sales_contact = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = ['Amount', 'Payment_Due', 'Title', 'Status', 'Date_created',
                  'Date_updated', 'id', 'sales_contact', 'client']

    def get_sales_contact(self, instance):
        queryset = instance.Sales_contact
        serializer = SalesSerializer(queryset)
        return serializer.data

    def get_client(self, instance):
        queryset = instance.Client
        serializer = ClientSerializer(queryset)
        return serializer.data


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['Title', 'Event_Date', 'Event_Status', 'id']


class CreateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['Title', 'Event_Date', 'Event_Status', 'Notes', 'Attendees', 'Contract', 'Support_contact']
        validators = [
            UniqueTogetherValidator(
                queryset=Event.objects.all(),
                fields=['Title', 'Contract']
            )
        ]


class UpdateEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['Title', 'Event_Date', 'Event_Status', 'Notes', 'Attendees', 'Contract', 'Support_contact']
        validators = [
            UniqueTogetherValidator(
                queryset=Event.objects.all(),
                fields=['Title', 'Contract']
            )
        ]


class EventDetailSerializer(serializers.ModelSerializer):

    contract = serializers.SerializerMethodField()
    support_contact = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = ['Title', 'Event_Date', 'Event_Status', 'Notes', 'Attendees', 'Date_created',
                  'Date_updated', 'id', 'contract', 'support_contact']

    def get_contract(self, instance):
        queryset = instance.Contract
        serializer = ContractDetailSerializer(queryset)
        return serializer.data

    def get_support_contact(self, instance):
        queryset = instance.Support_contact
        serializer = SupportSerializer(queryset)
        return serializer.data
