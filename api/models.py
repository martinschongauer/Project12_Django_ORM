from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


# null = False -> can't be created without this field
# CASCADE -> delete element if one of these users disappear
# related_name for the inverse relation


class User(AbstractUser):
    pass


class ManagementUser(models.Model):
    manager = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE,
                                related_name='manager_user')


class SalesUser(models.Model):
    seller = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE,
                               related_name='seller_user')


class SupportUser(models.Model):
    support = models.ForeignKey(to=User, null=False, on_delete=models.CASCADE,
                                related_name='support_user')


class Client(models.Model):

    First_name = models.fields.CharField(max_length=25, null=False)
    Last_name = models.fields.CharField(max_length=25, null=False)
    Email = models.fields.CharField(max_length=100, null=False)
    Phone = models.fields.CharField(max_length=20, null=False)
    Mobile = models.fields.CharField(max_length=20, null=False)
    Company_name = models.fields.CharField(max_length=250, null=False)
    Date_created = models.DateTimeField(auto_now_add=True)
    Date_updated = models.DateTimeField(auto_now=True)
    Sales_contact = models.ForeignKey(to=SalesUser, null=False, on_delete=models.CASCADE,
                                      related_name='client_sales_contact')
    Client_known = models.BooleanField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Email', 'Company_name'], name="client_unique")
        ]

    def __str__(self):
        return self.Email


class Contract(models.Model):

    Sales_contact = models.ForeignKey(to=SalesUser, null=False, on_delete=models.CASCADE,
                                      related_name='contract_sales_contract')
    Client = models.ForeignKey(to=Client, null=False, on_delete=models.CASCADE,
                               related_name='client_contract')
    Date_created = models.DateTimeField(auto_now_add=True)
    Date_updated = models.DateTimeField(auto_now=True)
    Status = models.BooleanField(null=False)
    Amount = models.FloatField(null=False)
    Payment_Due = models.IntegerField(default=60,
                                      validators=[MaxValueValidator(365), MinValueValidator(1)])
    Title = models.fields.CharField(max_length=100, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Title', 'Client'], name="contract_unique")
        ]

    def __str__(self):
        return self.Title


class Event(models.Model):

    STATUS = (
        ("Preparing", "Preparing"),
        ("Failure", "Failure"),
        ("Postponed", "Postponed"),
        ("Success", "Success"),
    )

    Contract = models.ForeignKey(to=Contract, null=False, on_delete=models.CASCADE,
                                 related_name='event_client')
    Date_created = models.DateTimeField(auto_now_add=True)
    Date_updated = models.DateTimeField(auto_now=True)
    Event_Status = models.fields.CharField(max_length=50, null=False, choices=STATUS)
    Support_contact = models.ForeignKey(to=SupportUser, null=False, on_delete=models.CASCADE,
                                        related_name='event_support_contact')
    Attendees = models.IntegerField(default=1,
                                    validators=[MaxValueValidator(1000), MinValueValidator(1)])
    Event_Date = models.fields.CharField(max_length=50, null=False)
    Title = models.fields.CharField(max_length=100)
    Notes = models.fields.CharField(max_length=10000)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Title', 'Contract'], name="event_unique")
        ]

    def __str__(self):
        return self.Title

