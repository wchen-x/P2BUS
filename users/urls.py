from django.urls import path
from .views import register, login_view, logout_view, forgot_password, reset_password, account_dashboard, profile, address_list, orders, wishlist

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('login/forgot_password/', forgot_password, name="forgot_password"),
    path('reset_password/<uidb64>/<token>/', reset_password, name="reset_password"),
    path('account/', account_dashboard, name='account_dashboard'),
    path("profile/", profile, name="profile"),
    path("addresses/", address_list, name="address_list"),
    path("orders/", orders, name="orders"),
    path("wishlist/", wishlist, name="wishlist"),
    path("logout/", logout_view, name="logout"),
]


