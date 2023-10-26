import datetime
import os
import qrcode
from PIL import Image
from pyzbar import pyzbar
from segno import helpers

# pip install qrcode, segno, pyzbar


# create wifi qrcode pic
# https://blog.csdn.net/chichu261/article/details/104460085
def create_wifi_qrcode(ssid, password, file_name, security="WPA/WPA2 PSK"):
    qr = helpers.make_wifi(ssid=ssid, 
					       password=password, 
					       security=security)
    qr.save(file_name, scale=10)
    return ("1", "ok")


# decode qrcode pic(get the information of the qrcode pic)
# https://blog.csdn.net/cungudafa/article/details/85871871
def decode_qrcode(code_img_path):
    if not os.path.exists(code_img_path):
        return ("0", "qrcode image is not exist, please check!")

    # Here, set only recognize QR Code and ignore other type of code
    results = pyzbar.decode(Image.open(code_img_path), symbols=[pyzbar.ZBarSymbol.QRCODE])
    return ("1", results[0].data.decode("utf-8"))
    

# make qrcode
def make_qr_code_no_icon(content):
    file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_make_qrcode_no_icon.png"
    # First, generate an usual QR Code image
    qr_code_maker = qrcode.QRCode(version=5,
                                  error_correction=qrcode.constants.ERROR_CORRECT_H,
                                  box_size=8,
                                  border=4,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    qr_code_img = qr_code_maker.make_image(fill_color="black", back_color="white").convert('RGBA')

    qr_code_img.save(file_name)  # 保存二维码图片
    # qr_code_img.show()  # 显示二维码图片
    return ("1", "ok")


# make qrcode with icon
def make_qr_code_with_icon(content, icon_path):
    if not os.path.exists(icon_path):
        return ("0", "icon image is not exist, please check!")

    file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_make_qrcode_with_icon.png"
    # First, generate an usual QR Code image
    qr_code_maker = qrcode.QRCode(version=5,
                                  error_correction=qrcode.constants.ERROR_CORRECT_H,
                                  box_size=8,
                                  border=4,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    qr_code_img = qr_code_maker.make_image(
        fill_color="black", back_color="white").convert('RGBA')

    # Second, load icon image and resize it
    icon_img = Image.open(icon_path)
    code_width, code_height = qr_code_img.size
    icon_img = icon_img.resize((code_width // 4, code_height // 4), Image.LANCZOS)

    # Last, add the icon to original QR Code
    qr_code_img.paste(icon_img, (code_width * 3 // 8, code_width * 3 // 8))

    qr_code_img.save(file_name)  # 保存二维码图片
    # qr_code_img.show()  # 显示二维码图片
    return ("1", "ok")


if __name__ == '__main__':
    # create wifi qrcode
    # wifi_file_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_wifi_qrcode.png"
    # print(create_wifi_qrcode("CMCC-7bZR", "2dt9s7me", wifi_file_name))
    
    # decode qrcode
    # print(decode_qrcode("vxjpg.jpg"))
    
    # make qrcode
    # print(make_qr_code_no_icon("hello dragon"))
    
    # make qrcode with icon
    print(make_qr_code_with_icon("hello dragon", "xxx.png"))
    
    
    
    
