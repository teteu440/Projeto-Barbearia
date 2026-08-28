from django.urls import path
from barbearia.views import index

urlpatterns = [
    path('',index),
]