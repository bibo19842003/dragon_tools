from django.urls import path
from . import views


app_name = 'tools'

urlpatterns =[
    path('', views.index, name='index'),
    path('index/', views.index),
    # qrcode
    path('create_wifi_qrcode_pic/', views.create_wifi_qrcode_pic, name="create_wifi_qrcode_pic"),
    path('decode_qr_code/', views.decode_qr_code, name="decode_qr_code"),

    path('image/', views.image, name="image"),
    path('resize_not_crop_1_image/', views.resize_not_crop_1_image, name="resize_not_crop_1_image"),
    path('resize_not_crop_more_image/', views.resize_not_crop_more_image, name="resize_not_crop_more_image"),
    path('resize_crop_1_image/', views.resize_crop_1_image, name="resize_crop_1_image"),
    path('resize_crop_more_image/', views.resize_crop_more_image, name="resize_crop_more_image"),
]
