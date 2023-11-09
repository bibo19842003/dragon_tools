import zipfile
import os
import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.conf import settings
from tools.dragon_qrcode import create_wifi_qrcode, decode_qrcode
from tools.handle_pic import resize_not_crop_1_pic, resize_not_crop_more_pic, resize_crop_1_pic, resize_crop_more_pic
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




@csrf_exempt
def image(request):
    return render(request, 'tools/image.html')
    

@csrf_exempt
def resize_not_crop_1_image(request):
    if request.method == 'GET':
        return render(request, 'tools/image.html', {"request":request})
    else:
        # 0 check input value
        r_width = request.POST.get('resize_not_crop_width', None)
        if r_width == None:
            # 16 目标图片宽度为空
            return JsonResponse({"res": 16})
        try:
            r_width = int(r_width)
        except:
            # 17 目标图片宽度输入不正确
            return JsonResponse({"res": 17})
            
        r_height = request.POST.get('resize_not_crop_height', None)
        if r_height == None:
            # 18 目标图片高度为空
            return JsonResponse({"res": 18})
        try:
            r_height = int(r_height)
        except:
            # 19 目标图片宽度输入不正确
            return JsonResponse({"res": 19})
        
        myfile = request.FILES.get('resize_not_crop_uploadfile', None)
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
        
        # 1 save upload file
        new_file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_" + myfile.name
        # new_file_name = myfile.name
        new_file_path = os.path.join(settings.MEDIA_ROOT, "tmp_handle_image_upload", new_file_name)
        
        with open(new_file_path, 'wb+') as f:
            for chunk in myfile.chunks():
                f.write(chunk)
            f.close()
            
        # 2 resize
        output_file_folder = os.path.join(settings.MEDIA_ROOT, "tmp_handle_image_result")
        result, ratio , i_width, i_height= resize_not_crop_1_pic(new_file_path, r_width, r_height, out_path=output_file_folder)
        
        if result:
            # success
            return JsonResponse({"res": 1, "pic_name": new_file_name, "ratio": ratio, "i_width": i_width, "i_height": i_height})
        else:
            # 目标尺寸大小 大于原始文件大小，不进行缩小操作
            return JsonResponse({"res": 2})




@csrf_exempt
def resize_not_crop_more_image(request):
    if request.method == 'GET':
        return render(request, 'tools/image.html', {"request":request})
    else:
        # 0 check input value
        r_width = request.POST.get('resize_not_crop_width_batch', None)
        if r_width == None:
            # 16 目标图片宽度为空
            return JsonResponse({"res": 16})
        try:
            r_width = int(r_width)
        except:
            # 17 目标图片宽度输入不正确
            return JsonResponse({"res": 17})
            
        r_height = request.POST.get('resize_not_crop_height_batch', None)
        if r_height == None:
            # 18 目标图片高度为空
            return JsonResponse({"res": 18})
        try:
            r_height = int(r_height)
        except:
            # 19 目标图片宽度输入不正确
            return JsonResponse({"res": 19})
            
        myfile = request.FILES.getlist('resize_not_crop_uploadfile_batch', None)
        if myfile == None:
            # return HttpResponse('----上传文件不能为空')
            # 10 文件为空
            return JsonResponse({"res": 10})
        
        # 1 save upload file
        time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        new_folder = os.path.join(settings.MEDIA_ROOT, "tmp_handle_image_upload", time_str)
        os.mkdir(new_folder)

        for i, u_file in enumerate(myfile):
            new_file_path = os.path.join(new_folder, u_file.name)
            with open(new_file_path, 'wb+') as f:
                for chunk in u_file.chunks():
                    f.write(chunk)
                f.close()

        # 2 resize
        output_file_folder = os.path.join(settings.MEDIA_ROOT, "tmp_handle_image_result", time_str)
        os.mkdir(output_file_folder)
        try:
            resize_not_crop_more_pic(new_folder, r_width, r_height, out_path=output_file_folder)
        except:
            # 批量操作失败
            return JsonResponse({"res": 3})
            
        # 3 zipfile
        os.chdir(output_file_folder)
        zip_file = output_file_folder + '.zip'
        zip = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
        for item in os.listdir(output_file_folder):
            zip.write(item)
        zip.close()

        return JsonResponse({"res": 1, "pic_name": time_str + ".zip"})



@csrf_exempt
def resize_crop_1_image(request):
    if request.method == 'GET':
        return render(request, 'tools/image.html', {"request":request})
    else:
        # 0 check input value
        r_width = request.POST.get('resize_crop_width', None)
        if r_width == None:
            # 16 目标图片宽度为空
            return JsonResponse({"res": 16})
        try:
            r_width = int(r_width)
        except:
            # 17 目标图片宽度输入不正确
            return JsonResponse({"res": 17})
            
        r_height = request.POST.get('resize_crop_height', None)
        if r_height == None:
            # 18 目标图片高度为空
            return JsonResponse({"res": 18})
        try:
            r_height = int(r_height)
        except:
            # 19 目标图片宽度输入不正确
            return JsonResponse({"res": 19})
        
        myfile = request.FILES.get('resize_crop_uploadfile', None)
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
        
        # 1 save upload file
        new_file_name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + "_" + myfile.name
        # new_file_name = myfile.name
        new_file_path = os.path.join(settings.MEDIA_ROOT, "tmp_handle_image_upload", new_file_name)
        
        with open(new_file_path, 'wb+') as f:
            for chunk in myfile.chunks():
                f.write(chunk)
            f.close()
            
        # 2 resize
        output_file_folder = os.path.join(settings.MEDIA_ROOT, "tmp_handle_image_result")
        result, ratio , i_width, i_height= resize_crop_1_pic(new_file_path, r_width, r_height, out_path=output_file_folder)
        
        if result:
            # success
            return JsonResponse({"res": 1, "pic_name": new_file_name, "ratio": ratio, "i_width": i_width, "i_height": i_height})
        else:
            # 目标尺寸大小 大于原始文件大小，不进行缩小操作
            return JsonResponse({"res": 2})




@csrf_exempt
def resize_crop_more_image(request):
    if request.method == 'GET':
        return render(request, 'tools/image.html', {"request":request})
    else:
        # 0 check input value
        r_width = request.POST.get('resize_crop_width_batch', None)
        if r_width == None:
            # 16 目标图片宽度为空
            return JsonResponse({"res": 16})
        try:
            r_width = int(r_width)
        except:
            # 17 目标图片宽度输入不正确
            return JsonResponse({"res": 17})
            
        r_height = request.POST.get('resize_crop_height_batch', None)
        if r_height == None:
            # 18 目标图片高度为空
            return JsonResponse({"res": 18})
        try:
            r_height = int(r_height)
        except:
            # 19 目标图片宽度输入不正确
            return JsonResponse({"res": 19})
            
        myfile = request.FILES.getlist('resize_crop_uploadfile_batch', None)
        if myfile == None:
            # return HttpResponse('----上传文件不能为空')
            # 10 文件为空
            return JsonResponse({"res": 10})
        
        # 1 save upload file
        time_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        new_folder = os.path.join(settings.MEDIA_ROOT, "tmp_handle_image_upload", time_str)
        os.mkdir(new_folder)

        for i, u_file in enumerate(myfile):
            new_file_path = os.path.join(new_folder, u_file.name)
            with open(new_file_path, 'wb+') as f:
                for chunk in u_file.chunks():
                    f.write(chunk)
                f.close()

        # 2 resize
        output_file_folder = os.path.join(settings.MEDIA_ROOT, "tmp_handle_image_result", time_str)
        os.mkdir(output_file_folder)
        try:
            resize_crop_more_pic(new_folder, r_width, r_height, out_path=output_file_folder)
        except:
            # 批量操作失败
            return JsonResponse({"res": 3})
            
        # 3 zipfile
        os.chdir(output_file_folder)
        zip_file = output_file_folder + '.zip'
        zip = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
        for item in os.listdir(output_file_folder):
            zip.write(item)
        zip.close()

        return JsonResponse({"res": 1, "pic_name": time_str + ".zip"})
