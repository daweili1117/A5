from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm

from .models import Customer, Item, Address, RentItems



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = '__all__'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's**6
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Customer
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'view_currency', 'is_active')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'itemAddedDate': forms.HiddenInput,
        }

    def clean_itemImage(self):
        itemImage = self.cleaned_data['itemImage']
        valid_extensions = ['jpg', 'jpeg']
        extension = itemImage.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given product Image file does not ' \
                                        'match valid image extensions.')
        return itemImage


class CreateAddressForm(forms.ModelForm):
    class Meta:
        model: Address
        fields = '__all__'


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Customer
        fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Customer
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')


class CustomUserSignupForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')


class DateInput(forms.DateInput):
    input_type = 'date'


class RentProductForm(ModelForm):
    class Meta:
        model = RentItems
        fields = ('item', 'rentStartDate', 'renterName', 'renterPhoneNumber')
        widgets = {
            'rentStartDate': DateInput(),
        }

    def __init__(self, user, *args, **kwargs):
        super(RentProductForm, self).__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(itemAvaialable=True, itemOwner=user)


class EndRentProductForm(ModelForm):
    class Meta:
        model = RentItems
        fields = ('item', 'rentStartDate', 'rentEndDate', 'notes')
        widgets = {
            'rentStartDate': DateInput(),
            'rentEndDate': DateInput(),
        }
