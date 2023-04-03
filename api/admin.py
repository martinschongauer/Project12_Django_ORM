from django.contrib import admin
from api.models import User, ManagementUser, SalesUser, SupportUser, Client, Contract, Event


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')


class ManagementUserAdmin(admin.ModelAdmin):
    list_display = ['manager']


class SalesUserAdmin(admin.ModelAdmin):
    list_display = ['seller']


class SupportUserAdmin(admin.ModelAdmin):
    list_display = ['support']


class ClientAdmin(admin.ModelAdmin):
    list_display = ('First_name', 'Last_name', 'Email', 'Company_name')


class ContractAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Payment_Due', 'Amount')


class EventAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Event_Date')


admin.site.register(User, UserAdmin)
admin.site.register(ManagementUser, ManagementUserAdmin)
admin.site.register(SalesUser, SalesUserAdmin)
admin.site.register(SupportUser, SupportUserAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Event, EventAdmin)
