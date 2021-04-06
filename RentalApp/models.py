from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
import requests


class Customer(AbstractUser):
    CURRENCIES = (
                     ('USD', _('United States Dollar')),
                     ('AED', _('United Arab Emirates Dirham')),
                     ('AFN', _('Afghan Afghani')),
                     ('ALL', _('Albanian Lek')),
                     ('AMD', _('Armenian Dram')),
                     ('ANG', _('Netherlands Antillean Guilder')),
                     ('AOA', _('Angolan Kwanza')),
                     ('ARS', _('Argentine Peso')),
                     ('AUD', _('Australian Dollar')),
                     ('AWG', _('Aruban Florin')),
                     ('AZN', _('Azerbaijani Manat')),
                     ('BAM', _('Bosnia-Herzegovina Convertible Mark')),
                     ('BBD', _('Barbadian Dollar')),
                     ('BDT', _('Bangladeshi Taka')),
                     ('BGN', _('Bulgarian Lev')),
                     ('BHD', _('Bahraini Dinar')),
                     ('BIF', _('Burundian Franc')),
                     ('BMD', _('Bermudan Dollar')),
                     ('BND', _('Brunei Dollar')),
                     ('BOB', _('Bolivian Boliviano')),
                     ('BRL', _('Brazilian Real')),
                     ('BSD', _('Bahamian Dollar')),
                     ('BTN', _('Bhutanese Ngultrum')),
                     ('BWP', _('Botswanan Pula')),
                     ('BZD', _('Belize Dollar')),
                     ('CAD', _('Canadian Dollar')),
                     ('CDF', _('Congolese Franc')),
                     ('CHF', _('Swiss Franc')),
                     ('CLF', _('Chilean Unit of Account UF')),
                     ('CLP', _('Chilean Peso')),
                     ('CNH', _('Chinese Yuan Offshore')),
                     ('CNY', _('Chinese Yuan')),
                     ('COP', _('Colombian Peso')),
                     ('CUP', _('Cuban Peso')),
                     ('CVE', _('Cape Verdean Escudo')),
                     ('CZK', _('Czech Republic Koruna')),
                     ('DJF', _('Djiboutian Franc')),
                     ('DKK', _('Danish Krone')),
                     ('DOP', _('Dominican Peso')),
                     ('DZD', _('Algerian Dinar')),
                     ('EGP', _('Egyptian Pound')),
                     ('ERN', _('Eritrean Nakfa')),
                     ('ETB', _('Ethiopian Birr')),
                     ('EUR', _('Euro')),
                     ('FJD', _('Fijian Dollar')),
                     ('FKP', _('Falkland Islands Pound')),
                     ('GBP', _('British Pound Sterling')),
                     ('GEL', _('Georgian Lari')),
                     ('GHS', _('Ghanaian Cedi')),
                     ('GIP', _('Gibraltar Pound')),
                     ('GMD', _('Gambian Dalasi')),
                     ('GNF', _('Guinean Franc')),
                     ('GTQ', _('Guatemalan Quetzal')),
                     ('GYD', _('Guyanaese Dollar')),
                     ('HKD', _('Hong Kong Dollar')),
                     ('HNL', _('Honduran Lempira')),
                     ('HRK', _('Croatian Kuna')),
                     ('HTG', _('Haitian Gourde')),
                     ('HUF', _('Hungarian Forint')),
                     ('IDR', _('Indonesian Rupiah')),
                     ('ILS', _('Israeli New Sheqel')),
                     ('INR', _('Indian Rupee')),
                     ('IQD', _('Iraqi Dinar')),
                     ('IRR', _('Iranian Rial')),
                     ('ISK', _('Icelandic Krona')),
                     ('JMD', _('Jamaican Dollar')),
                     ('JOD', _('Jordanian Dinar')),
                     ('JPY', _('Japanese Yen')),
                     ('KES', _('Kenyan Shilling')),
                     ('KGS', _('Kyrgystani Som')),
                     ('KHR', _('Cambodian Riel')),
                     ('KMF', _('Comorian Franc')),
                     ('KPW', _('North Korean Won')),
                     ('KRW', _('South Korean Won')),
                     ('KWD', _('Kuwaiti Dinar')),
                     ('KYD', _('Cayman Islands Dollar')),
                     ('KZT', _('Kazakhstani Tenge')),
                     ('LAK', _('Laotian Kip')),
                     ('LBP', _('Lebanese Pound')),
                     ('LKR', _('Sri Lankan Rupee')),
                     ('LRD', _('Liberian Dollar')),
                     ('LSL', _('Lesotho Loti')),
                     ('LYD', _('Libyan Dinar')),
                     ('MAD', _('Moroccan Dirham')),
                     ('MDL', _('Moldovan Leu')),
                     ('MGA', _('Malagasy Ariary')),
                     ('MKD', _('Macedonian Denar')),
                     ('MMK', _('Myanma Kyat')),
                     ('MNT', _('Mongolian Tugrik')),
                     ('MOP', _('Macanese Pataca')),
                     ('MRU', _('Mauritanian Ouguiya')),
                     ('MUR', _('Mauritian Rupee')),
                     ('MVR', _('Maldivian Rufiyaa')),
                     ('MWK', _('Malawian Kwacha')),
                     ('MXN', _('Mexican Peso')),
                     ('MYR', _('Malaysian Ringgit')),
                     ('MZN', _('Mozambican Metical')),
                     ('NAD', _('Namibian Dollar')),
                     ('NGN', _('Nigerian Naira')),
                     ('NOK', _('Norwegian Krone')),
                     ('NPR', _('Nepalese Rupee')),
                     ('NZD', _('New Zealand Dollar')),
                     ('OMR', _('Omani Rial')),
                     ('PAB', _('Panamanian Balboa')),
                     ('PEN', _('Peruvian Nuevo Sol')),
                     ('PGK', _('Papua New Guinean Kina')),
                     ('PHP', _('Philippine Peso')),
                     ('PKR', _('Pakistani Rupee')),
                     ('PLN', _('Polish Zloty')),
                     ('PYG', _('Paraguayan Guarani')),
                     ('QAR', _('Qatari Rial')),
                     ('RON', _('Romanian Leu')),
                     ('RSD', _('Serbian Dinar')),
                     ('RUB', _('Russian Ruble')),
                     ('RWF', _('Rwandan Franc')),
                     ('SAR', _('Saudi Riyal')),
                     ('SBD', _('Solomon Islands Dollar')),
                     ('SCR', _('Seychellois Rupee')),
                     ('SDG', _('Sudanese Pound')),
                     ('SEK', _('Swedish Krona')),
                     ('SGD', _('Singapore Dollar')),
                     ('SHP', _('Saint Helena Pound')),
                     ('SLL', _('Sierra Leonean Leone')),
                     ('SOS', _('Somali Shilling')),
                     ('SRD', _('Surinamese Dollar')),
                     ('SYP', _('Syrian Pound')),
                     ('SZL', _('Swazi Lilangeni')),
                     ('THB', _('Thai Baht')),
                     ('TJS', _('Tajikistani Somoni')),
                     ('TMT', _('Turkmenistani Manat')),
                     ('TND', _('Tunisian Dinar')),
                     ('TOP', _('Tongan Paanga')),
                     ('TRY', _('Turkish Lira')),
                     ('TTD', _('Trinidad and Tobago Dollar')),
                     ('TWD', _('New Taiwan Dollar')),
                     ('TZS', _('Tanzanian Shilling')),
                     ('UAH', _('Ukrainian Hryvnia')),
                     ('UGX', _('Ugandan Shilling')),
                     ('UYU', _('Uruguayan Peso')),
                     ('UZS', _('Uzbekistan Som')),
                     ('VND', _('Vietnamese Dong')),
                     ('VUV', _('Vanuatu Vatu')),
                     ('WST', _('Samoan Tala')),
                     ('XAF', _('CFA Franc BEAC')),
                     ('XCD', _('East Caribbean Dollar')),
                     ('XDR', _('Special Drawing Rights')),
                     ('XOF', _('CFA Franc BCEAO')),
                     ('XPF', _('CFP Franc')),
                     ('YER', _('Yemeni Rial')),
                     ('ZAR', _('South African Rand')),
                     ('ZMW', _('Zambian Kwacha')),
        )

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits \
                                 allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=30, blank=True)
    view_currency = models.CharField(default='USD', max_length=3, choices=CURRENCIES, verbose_name='View currency as')

    def price_offset(self):
        url = "https://api.fastforex.io/fetch-one"

        querystring = {"to": self.view_currency, "api_key": "68f5687c8e-31e1891ac4-qpki7m"}

        headers = {"Accept": "application/json"}

        response = requests.request("GET", url, headers=headers, params=querystring)

        datapull = response.json()

        conversion = float(datapull["result"][self.view_currency])

        return conversion


class Address(models.Model):
    addressId = models.AutoField(auto_created=True, primary_key=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, default=' ', null=True, blank=True,
                                    related_name='address')
    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
        blank=True
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    state = models.CharField(
        "State",
        max_length=1024
    )

    country = models.CharField(
        "Country",
        max_length=1024,
    )

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "%s" % self.addressId


class Category(models.Model):
    categoryId = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=1024)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return "%s" % self.name


class Item(models.Model):
    itemId = models.AutoField(auto_created=True, primary_key=True)
    itemName = models.CharField(
        "Name",
        max_length=1024,
    )
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='category'
                                 )
    itemImage = models.ImageField(upload_to='images', null=True, blank=True)
    itemOwner = models.ForeignKey(Customer,
                                  on_delete=models.CASCADE,
                                  related_name='my_items'

                                  )
    itemAvaialable = models.BooleanField()
    costPerItem = models.IntegerField(verbose_name='Cost per Item (USD)')
    itemDescription = models.TextField(null=True, blank=True)
    itemAddedDate = models.DateField(auto_now_add=True)
    asin = models.CharField(null=True, blank=True, max_length=10)

    def __str__(self):
        return "%s" % self.itemName

    def get_absolute_url(self):
        return reverse('RentalApp:item_details',
                       args=[self.itemId])

    def getcontact(self):
        return self.itemOwner.phone_number

    def getamazon(self):
        url = "https://amazon-live-data.p.rapidapi.com/getasin/us/" + str(self.asin)

        headers = {
            'x-rapidapi-key': "a58f03259cmsh602a38523c2fa13p16957ajsnb0b62b23c79f",
            'x-rapidapi-host': "amazon-live-data.p.rapidapi.com"
        }

        amzpull = requests.request("GET", url, headers=headers)

        amzparse = amzpull.json()

        amzdata = {'amzprice': float(amzparse["data"]["price"]),
        'amzname': amzparse["data"]["name"],
        'amzreviewrating': amzparse["data"]["review-rating"],
        'amzreviewcount': amzparse["data"]["review-count"],
        'amzprime': amzparse["data"]["isPrime"]
        }
        return amzdata


class RentItems(models.Model):
    rentId = models.AutoField(auto_created=True, primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    rentStartDate = models.DateField()
    rentEndDate = models.DateField(null=True)
    renterName = models.CharField(max_length=1024)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    renterPhoneNumber = models.CharField(validators=[phone_regex], max_length=30, blank=True)
    totalCost = models.FloatField(null=True)
    notes = models.TextField(null=True, blank=True)
    transactionID = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.rentId


# brew install graphviz
# pip install pyparsing pydot
# (venv) daweili@Daweis-MacBook-Pro MAH % python manage.py graph_models -a > erd.dot
# (venv) daweili@Daweis-MacBook-Pro MAH % python manage.py graph_models -a -g -o  ERD.png

from django.db import models

# Create your models here.
