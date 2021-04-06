import csv

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.forms import forms
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
from reportlab.lib.styles import getSampleStyleSheet
from twilio.rest import Client
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

from .models import Category, Item, Address, RentItems, Customer
from .forms import CustomUserSignupForm, RentProductForm, EndRentProductForm
import io
from reportlab.platypus import SimpleDocTemplate, Table
from .filters import ProductFilter

from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

import braintree

from django.contrib.auth.decorators import login_required


@login_required
def checkout_page(request):
    # generate all other required data that you may need on the #checkout page and add them to context.

    if settings.BRAINTREE_PRODUCTION:
        braintree_env = braintree.Environment.Production
    else:
        braintree_env = braintree.Environment.Sandbox

    # Configure Braintree
    braintree.Configuration.configure(
        braintree_env,
        merchant_id=settings.BRAINTREE_MERCHANT_ID,
        public_key=settings.BRAINTREE_PUBLIC_KEY,
        private_key=settings.BRAINTREE_PRIVATE_KEY,
    )

    try:
        braintree_client_token = braintree.ClientToken.generate({"customer_id": Customer.id})
    except:
        braintree_client_token = braintree.ClientToken.generate({})

    context = {'braintree_client_token': braintree_client_token}
    return render(request, 'checkout.html', context)





def item_list(request):
    categories = Category.objects.all()
    items = Item.objects.filter(itemAvaialable=True)
    request.session["addressId"] = None
    searchFilter = ProductFilter(request.GET, queryset=items)
    items = searchFilter.qs
    if not request.user.is_anonymous:
        try:
            addresses = Address.objects.filter(customer=request.user)
            for add in addresses:
                address = get_object_or_404(Address, addressId=add.addressId)
                request.session["addressId"] = address.addressId
        except Address.DoesNotExist:
            address = None

    user = None
    if request.user.is_authenticated:
        user = request.user
        currency = user.view_currency
    else:
        currency = 'USD'

    if currency != 'USD':
        offset = round(user.price_offset(), 4)
        for item in items:
            item.costPerItem = round(item.costPerItem * offset, 2)

    return render(request,
                  'home.html',
                  {'categories': categories,
                   'items': items,
                   'filter': searchFilter,
                   'currency' : currency})


def item_details(request, id):
    item = get_object_or_404(Item,
                             itemId=id)

    if item.asin is not None:
        amazondetails = Item.getamazon(item)
    else:
        amazondetails = None

    user = None
    if request.user.is_authenticated:
        user = request.user
        currency = user.view_currency
    else:
        currency = 'USD'

    if currency != 'USD':
        offset = round(user.price_offset(), 4)
        if amazondetails is not None:
            amazondetails['amzprice'] = round(amazondetails['amzprice'] * offset, 2)
        item.costPerItem = round(item.costPerItem * offset, 2)

    return render(request,
                  'itemDetails.html',
                  {'item': item, 'amazondetails': amazondetails, 'currency': currency,})


@login_required(login_url='/users/login/')
def product_details(request, id):
    item = get_object_or_404(Item,
                             itemId=id)
    return render(request,
                  'productDetails.html',
                  {'item': item})


class AddressView(LoginRequiredMixin, DetailView):
    model = Address
    template_name = 'address.html'
    login_url = '/users/login/'

    def form_valid(self, form):
        form.is_valid()
        form.instance.customer = self.request.user
        return super().form_valid(form)


class UpdateAddressView(LoginRequiredMixin, UpdateView):
    model = Address
    template_name = 'editAddress.html'
    fields = ('address1', 'address2', 'zip_code', 'city', 'country')
    login_url = '/users/login/'

    def form_valid(self, form):
        form.is_valid()
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('RentalApp:address', args=[self.request.user.address.pk])


class AddAddressView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'addAddress.html'
    fields = ('address1', 'address2', 'zip_code', 'city', 'state', 'country')
    login_url = '/users/login/'

    def form_valid(self, form):
        form.is_valid()
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('RentalApp:item_list')


class SignUpView(CreateView):
    form_class = CustomUserSignupForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required(login_url='/users/login/')
def PasswordChangeView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('changePassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/changePassword.html', {
        'form': form
    })


@login_required(login_url='/users/login/')
def myProducts(request):
    address = None
    try:
        addresses = Address.objects.filter(customer=request.user)
        for add in addresses:
            address = get_object_or_404(Address, addressId=add.addressId)
    except Address.DoesNotExist:
        address = None

    if not request.user.is_anonymous:
        items = Item.objects.filter(itemOwner=request.user)
    else:
        items = None

    return render(request,
                  'myProducts.html',
                  {'items': items,
                   'address': address})


class AddProductView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'addProduct.html'
    image = forms.FileField(required=False)
    fields = ('itemName',
              'category',
              'itemImage',
              'itemAvaialable',
              'costPerItem',
              'itemDescription')
    login_url = '/users/login/'

    def form_valid(self, form):
        form.is_valid()
        form.instance.itemOwner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('RentalApp:my_products')


class EditProductView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'editProduct.html'
    login_url = '/users/login/'
    fields = ('itemName',
              'category',
              'itemImage',
              'itemAvaialable',
              'costPerItem',
              'itemDescription')

    def form_valid(self, form):
        form.is_valid()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('RentalApp:my_products')


class DeleteProductView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'deleteProduct.html'
    success_url = reverse_lazy('RentalApp:my_products')
    login_url = '/users/login/'


class StartRentView(LoginRequiredMixin, CreateView):
    form_class = RentProductForm
    template_name = 'rental.html'
    success_url = reverse_lazy('RentalApp:rental_history')
    login_url = '/users/login/'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user.id
        return kwargs

    def form_valid(self, form):
        form.is_valid()
        item = get_object_or_404(Item, itemId=form.instance.item.itemId)
        item.itemAvaialable = False
        item.save()
        # form.instance.item = item
        return super().form_valid(form)


class RentalHisoryView(LoginRequiredMixin, ListView):
    template_name = 'rentalHist.html'
    login_url = '/users/login/'

    def get(self, request):
        items = Item.objects.filter(itemOwner=request.user)
        rent_items = RentItems.objects.filter(item__in=items)
        return render(request, self.template_name,
                      {'rent_items': rent_items})


class updateRentItemView(LoginRequiredMixin, UpdateView):
    model = RentItems
    form_class = EndRentProductForm
    template_name = 'rentEnd.html'
    login_url = '/users/login/'

    def form_valid(self, form):
        form.is_valid()
        item = get_object_or_404(Item, itemId=form.instance.item.itemId)
        rent = item.costPerItem
        item.itemAvaialable = True
        item.save()
        days = (form.instance.rentEndDate - form.instance.rentStartDate).days
        form.instance.totalCost = days * rent
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('RentalApp:rent_overView', kwargs={'pk': self.object.pk})


class rentDetailView(LoginRequiredMixin, DetailView):
    model = RentItems
    template_name = 'rentOverView.html'
    login_url = '/users/login/'


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="rental_history.csv"'
    writer = csv.writer(response)
    writer.writerow(
        ['ItemName', 'RentstartDate', 'RentEndDate', 'Totalcost', 'RenterName', 'RenterPhoneNumber', 'Notes'])
    item_list = Item.objects.filter(itemOwner=request.user)
    rentItems = RentItems.objects.filter(item__in=item_list)
    for item in rentItems:
        writer.writerow([item.item.itemName, item.rentStartDate, item.rentEndDate, item.totalCost, item.renterName,
                         item.renterPhoneNumber, item.notes])
    return response


def export_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()
    data = []
    my_doc = SimpleDocTemplate(buffer)
    sample_style_sheet = getSampleStyleSheet()
    data += [['Rental History']]
    item_list = Item.objects.filter(itemOwner=request.user)
    rentItems = RentItems.objects.filter(item__in=item_list)
    data += [['ItemName', 'RentStartDate', 'RentEndDate', 'RenterName', 'Renter Phonenumber', 'Notes', 'TotalRent']]
    for i in rentItems:
        itemName = str(i.item.itemName).encode('utf-8')
        rentStartDate = str(i.rentStartDate).encode('utf-8')
        renterName = str(i.renterName).encode('utf-8')
        renterPhoneNumber = str(i.renterPhoneNumber).encode('utf-8')
        notes = str(i.notes).encode('utf-8')
        rentEndDate = str(i.rentEndDate).encode('utf-8')
        totalCost = str(i.totalCost).encode('utf-8')

        # Add this loop's step row into data array
        data += [[itemName, rentStartDate, rentEndDate, renterName, renterPhoneNumber, notes, totalCost]]

    table_data = Table(data, colWidths=None, rowHeights=None)
    my_doc.build([table_data])
    # Create the PDF object, using the buffer as its "file."
    pdf_value = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rental_history.pdf"'

    response.write(pdf_value)
    return response


class EditAccountInfoView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'accountDetails.html'
    login_url = '/users/login/'
    fields = ('first_name',
              'last_name',
              'email',
              'phone_number',
              'view_currency')

    def get_success_url(self):
        return reverse('RentalApp:item_list')

    def form_valid(self, form):
        form.is_valid()
        return super().form_valid(form)

def sendMail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    renter = request.POST['username']
    email = request.POST['email']
    message = request.POST['message']
    ctx = {
        'itemId' : item.pk,
        'renter': renter,
        'email': email,
        'message': message
    }
    subject = renter+" is interested in your product "+item.itemName
    message = render_to_string('conatctowner.html', ctx, request=request)
    emails = [item.itemOwner.email]

    msg = EmailMessage(subject, message, settings.EMAIL_HOST_USER, emails)
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send(fail_silently=False)
    if item.itemOwner.phone_number:
        checkSMS = request.POST['sendSMS']
        if checkSMS:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body="Hi, " + renter + " is intrested in your product "+item.itemName+". Conact information of "+renter+" is: "+email,
                from_= settings.TWILIO_PHONE_NUMBER,
                to= item.itemOwner.phone_number
            )
    return redirect('RentalApp:item_details',id=pk)

