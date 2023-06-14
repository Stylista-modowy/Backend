import cv2
import numpy as np
from PIL import Image, ImageChops
from enum import Enum
 
class ClothesType(Enum):
    LongSleeveShirts = "Long Sleeve Shirts",
    ShortSleeveShirts= "Short Sleeve Shirts",
    Tops = "Tops",
    Trousers = "Trousers",
    Shorts = "Shorts",
    Dresses = "Dresses",
    Skirts = "Skirts",
    Shoes = "Shoes",
    Heels = "Heels"

class Gender(Enum):
    Male = "Male",
    Female = "Female"
	

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def put_on_image(im, back, type, gender):
    if gender == Gender.Male:
        if type == ClothesType.ShortSleeveShirts:
            hpercent = (285/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize,285), Image.Resampling.LANCZOS)
            back.paste(im, (235, 200), im)
        elif type == ClothesType.LongSleeveShirts:
            hpercent = (285/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize,285), Image.Resampling.LANCZOS)
            back.paste(im, (130, 220), im)
        elif type == ClothesType.Trousers:
            wpercent = (165/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            im = im.resize((165,hsize), Image.Resampling.LANCZOS)
            back.paste(im, (275, 460), im)  
        elif type == ClothesType.Shorts:
            wpercent = (165/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            im = im.resize((165,hsize), Image.Resampling.LANCZOS)
            back.paste(im, (275, 460), im)  
        elif type == ClothesType.Shoes:
            hpercent = (80/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize,80), Image.Resampling.LANCZOS)
            back.paste(im, (470, 850), im)
    elif gender == Gender.Female:
        if type == ClothesType.ShortSleeveShirts:
            hpercent = (285/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize,285), Image.Resampling.LANCZOS)
            back.paste(im, (190, 200), im)
        elif type == ClothesType.LongSleeveShirts:
            hpercent = (285/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize,285), Image.Resampling.LANCZOS)
            back.paste(im, (90, 210), im)
        elif type == ClothesType.Trousers:
            wpercent = (165/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            im = im.resize((165,hsize), Image.Resampling.LANCZOS)
            back.paste(im, (240, 420), im)  
        elif type == ClothesType.Shorts:
            wpercent = (165/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            im = im.resize((165,hsize), Image.Resampling.LANCZOS)
            back.paste(im, (240, 420), im)  
        elif type == ClothesType.Tops:
            hpercent = (200/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize,200), Image.Resampling.LANCZOS)
            back.paste(im, (235, 210), im)
        elif type == ClothesType.Skirts:
            wpercent = (300/float(im.size[0]))
            hsize = int((float(im.size[1])*float(wpercent)))
            im = im.resize((300,hsize), Image.Resampling.LANCZOS)
            back.paste(im, (170, 420), im)  
        elif type == ClothesType.Dresses:
            hpercent = (460/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize,460), Image.Resampling.LANCZOS)
            back.paste(im, (130, 210), im)
        elif type == ClothesType.Shoes:
            hpercent = (80/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize,80), Image.Resampling.LANCZOS)
            back.paste(im, (450, 850), im)
        elif type == ClothesType.Heels:
            hpercent = (80/float(im.size[1]))
            wsize = int((float(im.size[0])*float(hpercent)))
            im = im.resize((wsize,80), Image.Resampling.LANCZOS)
            back.paste(im, (450, 850), im)
    return back


# im1 = Image.open('shoes/out.png')
# back = Image.open("maleT-pose.jpeg")
# # back = Image.open("femaleT-pose.jpeg")
# type = ClothesType.Shoes
# gender = Gender.Male
# im1 = trim(im1)
# im2 = put_on_image(im1, back, type, gender)


# im2.save("result.png")

