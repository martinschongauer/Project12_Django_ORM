from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import datetime

from api.models import ManagementUser, SalesUser, SupportUser, Client, Contract, Event

UserModel = get_user_model()


class Command(BaseCommand):

    help = 'Initialize project for local development'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        # Clean a little bit
        ManagementUser.objects.all().delete()
        SalesUser.objects.all().delete()
        SupportUser.objects.all().delete()
        Client.objects.all().delete()
        Contract.objects.all().delete()
        Event.objects.all().delete()
        UserModel.objects.all().delete()

        # Add users
        admin = UserModel.objects.create_superuser(username='admin@oc.com',
                                                   first_name='Super', last_name='User',
                                                   email='admin@oc.com', password='password')
        user1 = UserModel.objects.create_user(username='baptistehornecker@oc.com',
                                              first_name='Baptiste', last_name='Hornecker',
                                              email='baptistehornecker@oc.com', password='password')
        user2 = UserModel.objects.create_user(username='paveldurov@oc.com',
                                              first_name='Pavel', last_name='Durov',
                                              email='paveldurov@oc.com', password='password')
        user3 = UserModel.objects.create_user(username='anonymous@oc.com',
                                              first_name='Ano', last_name='Nymous',
                                              email='anonymous@oc.com', password='password')
        user4 = UserModel.objects.create_user(username='supportone@oc.com',
                                              first_name='Support', last_name='One',
                                              email='supportone@oc.com', password='password')
        user5 = UserModel.objects.create_user(username='supporttwo@oc.com',
                                              first_name='Support', last_name='Two',
                                              email='supporttwo@oc.com', password='password')

        # Confirm at least that users have been created as expected
        print(f"admin id: {admin.id}")
        print(f"user1 id: {user1.id}")
        print(f"user2 id: {user2.id}")
        print(f"user3 id: {user3.id}")
        print(f"user2 id: {user4.id}")
        print(f"user3 id: {user5.id}")

        # Sort users into the three role tables
        manager1 = ManagementUser.objects.create(manager=user1)
        seller1 = SalesUser.objects.create(seller=user2)
        seller2 = SalesUser.objects.create(seller=user3)
        support1 = SupportUser.objects.create(support=user4)
        support2 = SupportUser.objects.create(support=user5)

        # Add a potential client and two existing clients
        apple = Client.objects.create(First_name='Steve',
                                      Last_name='Jobs',
                                      Email='Steve.Jobs@apple.com',
                                      Phone='01 23 45 67 89',
                                      Mobile='06 23 45 67 89',
                                      Company_name='Apple',
                                      Sales_contact=seller1,
                                      Client_known=False
                                      )

        microsoft = Client.objects.create(First_name='Bill',
                                          Last_name='Gates',
                                          Email='Bill.Gates@Microsoft.com',
                                          Phone='01 06 06 06 06',
                                          Mobile='06 06 06 06 06',
                                          Company_name='Microsoft',
                                          Sales_contact=seller2,
                                          Client_known=True
                                          )

        google = Client.objects.create(First_name='Larry',
                                       Last_name='Page',
                                       Email='Larry.Page@gmail.com',
                                       Phone='01 00 00 00 00',
                                       Mobile='06 00 00 00 00',
                                       Company_name='google',
                                       Sales_contact=seller1,
                                       Client_known=True
                                       )

        # Add a contract and an event for every client
        contract1 = Contract.objects.create(Sales_contact=google.Sales_contact,
                                            Client=google,
                                            Status=True,
                                            Amount=100.0,
                                            Payment_Due=60,
                                            Title='New Year celebration - contract',
                                            )

        contract2 = Contract.objects.create(Sales_contact=microsoft.Sales_contact,
                                            Client=microsoft,
                                            Status=True,
                                            Amount=1000.0,
                                            Payment_Due=60,
                                            Title='New Product party - contract',
                                            )

        event1 = Event.objects.create(Contract=contract1,
                                      Event_Status="Preparing",
                                      Support_contact=support1,
                                      Attendees=200,
                                      Event_Date="12/31/2023",
                                      Title='New Year celebration',
                                      Notes='Notes to be added for the new year',
                                      )

        event2 = Event.objects.create(Contract=contract2,
                                      Event_Status="Postponed",
                                      Support_contact=support2,
                                      Attendees=150,
                                      Event_Date="12/15/2023",
                                      Title='New Product party',
                                      Notes='To be filled later',
                                      )

        self.stdout.write(self.style.SUCCESS("All Done !"))
