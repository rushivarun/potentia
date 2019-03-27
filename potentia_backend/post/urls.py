from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = "post"

urlpatterns = [
    url(r'addtrans/', views.add_transaction, name="Add_Trans"),
    url(r'MyTrans/',views.my_trans, name="My_Trans"),

]