from django.urls import path
from .views import register, login_view, forgot_password, reset_password

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login_view'),
    path('login/forgot_password/', forgot_password, name="forgot_password"),
    path('reset_password/', reset_password, name="reset_password")
]
