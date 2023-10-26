import os
import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from tools.dragon_qrcode import create_wifi_qrcode, decode_qrcode
# Create your views here.


pic_suffix_list = ["jpg", "jpeg", "png", "bmp"]



# homepage
def index(request):
    return render(request, 'index.html')
    


@csrf_exempt
def create_wifi_qrcode_pic(request):
    if request.method == 'GET':
        return render(request, 'tools/create_wifi_qrcode_pic.html')
    else:
        wifi_name = request.POST.get('wifi_name')
        wifi_pass = request.POST.get('wifi_pass')

        wifi_pic_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "_wifi_qrcode.png"
        wifi_pic_path = os.path.join(settings.MEDIA_ROOT, "wifi_pic", wifi_pic_name)
        _, _ = create_wifi_qrcode(wifi_name, wifi_pass, wifi_pic_path)
        

        return JsonResponse({"res": 1, "pic_name": wifi_pic_name})

    


@csrf_exempt
def decode_qr_code(request):
    if request.method == 'GET':
        return render(request, 'tools/decode_qr_code.html', {"request":request})
    else:
        myfile = request.FILES.get('uploadfile', None)
        if myfile == None:
            # return HttpResponse('----上传文件不能为空')
            # 10 文件为空
            return JsonResponse({"res": 10})
        # 文件后缀名判断
        file_suffix = myfile.name.split(".")[-1]

        if file_suffix.lower() not in pic_suffix_list:
            # return HttpResponse('----文件后缀名不正确')
            # 11 文件名后缀不正确
            return JsonResponse({"res": 11})
        
        # 1 保存文件
        new_file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_" + myfile.name
        # new_file_name = myfile.name
        new_file_path = os.path.join(settings.MEDIA_ROOT, "tmp", new_file_name)
        
        with open(new_file_path, 'wb+') as f:
            for chunk in myfile.chunks():
                f.write(chunk)
            f.close()
            
        # 2 解码
        try:
            _, contents = decode_qrcode(new_file_path)
        except:
            return JsonResponse({"res": 20, "content": "无法解码此文件"})

        return JsonResponse({"res": 1, "content": contents})





