from os.path import dirname,join
from PIL import Image
from io import BytesIO
import base64
import os
import random
import json


path = dirname(__file__)
abspath = dirname(path)

def gacha_loader():
    with open(join(path,"gacha.json"), encoding='utf-8') as fp:
        data = json.load(fp)
    return data

def run_gacha():
    result = []
    pool = gacha_loader()
    purple_gift = pool["purple_gift"]
    purple_flag = 0
    for i in range (0,10):
        result.append(single_pull(pool))
        if result[i][0] < 80 and (result[i][1] not in purple_gift):
            purple_flag = purple_flag + 1
    if purple_flag == 10 and result[9][0] <= 95:
        result[9][0] = 1
        result[9][1] = purple_gift[random.randint(0, len(purple_gift) - 1)]
    return concat_images(result)


def single_pull(pool):
    up_pool = []
    for i in range (0,len(pool["up"])):
        up_pool.append(pool["up"][i] + ".png")
    normal_pool = []
    for i in range (0,len(pool["normal"])):
        normal_pool.append(pool["normal"][i] + ".png")


    gift_list = file_loader("gift")  # 读取礼物
    decoration = file_loader("decoration")  # 读取特效装扮
    person = file_loader("person")  # 读取人物

    objint = random.randint(1,100)
    if objint < 80:
        prop = gift_list[random.randint(0, len(gift_list)-1)]
    elif objint >= 80 and objint <= 95:
        prop = decoration[random.randint(0, len(decoration)-1)]
    else:
        objint_person = random.randint(1,100)
        if objint_person <=51:
            prop = up_pool[random.randint(0, len(up_pool)-1)]
        else:
            prop = normal_pool[random.randint(0, len(normal_pool) - 1)]
    data = []
    data.append(objint)
    data.append(prop)
    return data

def file_loader(file_type):
    filelist = []
    for filename in os.walk(abspath + "/resources/" + file_type):
        filelist.append(filename)
    return filelist[0][2]

def concat_images(image):
    COL = 5  # 指定拼接图片的列数
    ROW = 2  # 指定拼接图片的行数
    UNIT_HEIGHT_SIZE = 266  # 图片高度
    UNIT_WIDTH_SIZE = 266  # 图片宽度
    image_names = []
    for tmp_image in image:
        image_names.append(tmp_image[1])
    image_files = []
    for index in range(COL * ROW):
        if image[index][0] < 80:
            imgpath = abspath + "/resources/gift/"
        elif image[index][0] > 95:
            imgpath = abspath + "/resources/person/"
        else:
            imgpath = abspath + "/resources/decoration/"
        img = Image.open(imgpath + image_names[index])
        img = img.resize((256, 256), Image.ANTIALIAS)
        image_files.append(img)  # 读取所有用于拼接的图片

    target = Image.new('RGB', (UNIT_WIDTH_SIZE * COL+10, UNIT_HEIGHT_SIZE * ROW+10),(0,0,0,0))  # 创建成品图的画布
    for row in range(ROW):
        for col in range(COL):
            target.paste(image_files[COL * row + col], (10 + UNIT_WIDTH_SIZE * col, 10 + UNIT_HEIGHT_SIZE * row))
    return pil2b64(target)

def pil2b64(data):
    bio = BytesIO()
    data = data.convert("RGB")
    data.save(bio, format='JPEG', quality=75)
    base64_str = base64.b64encode(bio.getvalue()).decode()
    return 'base64://' + base64_str
