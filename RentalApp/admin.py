
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm, UserCreationForm
from .models import Customer, Address, Category, Item, RentItems

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')}
        ),
    )

class AddressAdmin(admin.ModelAdmin):
   model = Address
   list_display = ['customer',
                   'address1',
                   'address2',
                   'zip_code',
                   'city',
                   'country']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name']

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ['itemName',
                    'category',
                    'itemImage',
                    'itemOwner',
                    'itemAvaialable',
                    'costPerItem',
                    'itemDescription',
                    'itemAddedDate']

class RentItemsAdmin(admin.ModelAdmin):
    model = RentItems
    list_display = ['item',
                    'rentStartDate',
                    'rentEndDate',
                    'renterName',
                    'renterPhoneNumber',
                    'totalCost'
                    ]


admin.site.register(Customer, UserAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(RentItems,RentItemsAdmin)
from django.contrib import admin

# Register your models here.
