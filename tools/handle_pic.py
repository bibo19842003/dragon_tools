import os
from PIL import Image



# resize picture base width or r_height for 1 pic
def resize_not_crop_1_pic(image, r_width, r_height, out_path=None):
    img = Image.open(image)
    i_width, i_height = img.size
    
    # if image size less then input size, then return None.
    if i_width < r_width or i_height < r_height:
        return None, None, None, None
        
    i_ratio = '{:.2f}'.format(i_width / i_height)
    r_ratio = '{:.2f}'.format(r_width / r_height)
    
    # 1 get ratio
    if i_ratio > r_ratio:
        # base height
        ratio = float('{:.2f}'.format(i_height / r_height))
    else:
        # base width
        ratio = float('{:.2f}'.format(i_width / r_width))
        
    # 2 resize
    img_resized = img.resize((int(i_width / ratio), int(i_height / ratio)))
    
    # save
    if out_path:
        image_path, image_name = os.path.split(image)
        img_resize_name = os.path.join(out_path, image_name)
    else:
        img_resize_name = image.split(".")[0] + "_resize." + image.split(".")[-1]
        
    img_resized.save(img_resize_name)
    
    return True, ratio, i_width, i_height
    

# resize picture base width or r_height for many images
def resize_not_crop_more_pic(in_path, r_width, r_height, out_path=None):
    pic_suffix_list = ["jpg", "jpeg", "png", "bmp", "gif"]
    if os.path.isdir(in_path):
        for i in os.listdir(in_path):
            if "." in i:
                file_suffix = i.split(".")[-1]
                if file_suffix.lower() in pic_suffix_list:
                    resize_not_crop_1_pic(os.path.join(in_path, i), r_width, r_height, out_path=out_path)


# resize and crop pic to width and height for 1 pic
def resize_crop_1_pic(image, r_width, r_height, out_path=None):
    img = Image.open(image)
    i_width, i_height = img.size
    
    # if image size less then input size, then return None.
    if i_width < r_width or i_height < r_height:
        return None, None, None, None
        
    i_ratio = '{:.2f}'.format(i_width / i_height)
    r_ratio = '{:.2f}'.format(r_width / r_height)
    
    crop_width = False
    
    # 1 get ratio
    if i_ratio > r_ratio:
        # base height
        ratio = float('{:.2f}'.format(i_height / r_height))
        crop_width = True
    else:
        # base width
        ratio = float('{:.2f}'.format(i_width / r_width))
        
    # 2 resize
    resize_width = int(i_width / ratio)
    resize_height = int(i_height / ratio)
    img_resized = img.resize((resize_width, resize_height))
    
    # 3 crop
    if crop_width:
        width_more = resize_width - r_width
        img_resized = img_resized.crop((int(width_more / 2), 0, resize_width - int(width_more / 2), resize_height))  # (left, upper, right, lower)
    else:
        height_more = resize_height - r_height
        img_resized = img_resized.crop((0, int(height_more / 2), resize_width, resize_height - int(height_more / 2)))  # (left, upper, right, lower)
        
    # save
    if out_path:
        image_path, image_name = os.path.split(image)
        img_resize_name = os.path.join(out_path, image_name)
    else:
        img_resize_name = image.split(".")[0] + "_resize." + image.split(".")[-1]
        
    img_resized.save(img_resize_name)
    
    return True, ratio, i_width, i_height


# resize and crop pic to width and height for many images
def resize_crop_more_pic(in_path, r_width, r_height, out_path=None):
    pic_suffix_list = ["jpg", "jpeg", "png", "bmp", "gif"]
    if os.path.isdir(in_path):
        for i in os.listdir(in_path):
            if "." in i:
                file_suffix = i.split(".")[-1]
                if file_suffix.lower() in pic_suffix_list:
                    resize_crop_1_pic(os.path.join(in_path, i), r_width, r_height, out_path=out_path)
                    


if __name__ == "__main__":
    image = "shibie/001.jpg"
    in_path = "shibie/sure2"
    # resize_not_crop_1_pic(image, 768, 512, out_path=None)
    # resize_not_crop_more_pic(in_path, 768, 512, out_path=None)
    # resize_crop_1_pic(image, 768, 512, out_path=None)
    # resize_crop_more_pic(in_path, 768, 512, out_path=None)

