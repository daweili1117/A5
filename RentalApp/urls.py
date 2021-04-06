from django.urls import path
from .views import (
    AddAddressView,
    SignUpView,
    UpdateAddressView,
    AddProductView,
    EditProductView,
    DeleteProductView,
    AddressView,
    item_list,
    myProducts,item_details,
    product_details,
    StartRentView,
    RentalHisoryView,
    updateRentItemView,
    rentDetailView,
    export_pdf,
    export_csv,
    EditAccountInfoView,
    sendMail,
    checkout_page
)
from django.contrib.auth import views as auth_views

app_name = 'RentalApp'
urlpatterns = [
    path('', item_list, name='item_list'),
    path('myproducts/',myProducts, name='my_products'),
    path('export_pdf/',export_pdf,name='export_pdf'),
    path('export_csv/',export_csv,name='export_csv'),
    path('item/<int:id>/', item_details,name='item_details'),
    path('product/<int:id>', product_details, name='product_details'),
    path('address/<int:pk>/',AddressView.as_view(),name='address'),
    path('product/add/',AddProductView.as_view(), name='add_product'),
    path('product/<int:pk>/edit/',EditProductView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/',DeleteProductView.as_view(), name='delete_product'),
    path('add/', AddAddressView.as_view(), name="add_address"),
    path('<int:pk>/edit/', UpdateAddressView.as_view(), name="edit_address"),
    path('rent/',StartRentView.as_view(), name='rent'),
    path('rentals/',RentalHisoryView.as_view(),name='rental_history'),
    path('<int:pk>/endRent',updateRentItemView.as_view(),name='end_rent'),
    path('<int:pk>/rentOverview',rentDetailView.as_view(),name='rent_overView'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('changePassword/', auth_views.PasswordChangeView.as_view(
        template_name = 'registration/changePassword.html',
        success_url = '/'
    ), name='changePassword'),
    path('<int:pk>/accountDetails/',EditAccountInfoView.as_view(),name='accountDetails'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('sendMail/<int:pk>/',sendMail,name="send_email"),

    path('item/checkout/', checkout_page, name='checkout_page'),


    # url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    # url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
]