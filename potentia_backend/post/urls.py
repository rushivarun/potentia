from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

app_name = "post"

urlpatterns = [
    url(r'addtrans/', views.add_transaction, name="Add_Trans"),
    url(r'MyTrans/',views.my_trans, name="My_Trans"),
    url(r'AvailTrans/',views.open_trans.as_view(), name="Open_Trans"),
    url(r'^AvailTrans/(?P<pk>\d+)/$', views.make_trans, name="Make_Trans"),

]