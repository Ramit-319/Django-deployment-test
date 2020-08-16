
from django.urls import path
from django.urls import include
from protect import views

app_name = 'protect'

urlpatterns = [
    path('register/' , views.register ,  name = 'register'),
    path('user_login/' , views.user_login , name = 'userlogin'),
]
