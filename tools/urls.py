from django.urls import path
from . import views


app_name = 'tools'

urlpatterns =[
    path('', views.index, name='index'),
    path('index/', views.index),
    # qrcode
    path('create_wifi_qrcode_pic/', views.create_wifi_qrcode_pic, name="create_wifi_qrcode_pic"),
    path('decode_qr_code/', views.decode_qr_code, name="decode_qr_code"),

]
