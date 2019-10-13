import numpy as np
import cv2
import matplotlib.pyplot as plt

def imread_photo(filename,flags = cv2.IMREAD_COLOR ):
    return  cv2.imread(filename,flags)

def resize_photo(imgArr,MAX_WIDTH = 1000):
    img = imgArr
    rows, cols= img.shape[:2]     #获取输入图像的高和宽
    if cols >  MAX_WIDTH:
        change_rate = MAX_WIDTH / cols
        img = cv2.resize(img ,( MAX_WIDTH ,int(rows * change_rate) ), interpolation = cv2.INTER_AREA)
    return img

img = imread_photo("C:\\Users\\Samson\\Desktop\\doornum.jpg")

#gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

imageArr = resize_photo(img)

img_copy = imageArr.copy()

gray_img = cv2.cvtColor(img_copy , cv2.COLOR_BGR2GRAY)

gray_img_ = cv2.GaussianBlur(gray_img, (5,5), 0, 0, cv2.BORDER_DEFAULT)

kernel = np.ones((23, 23), np.uint8)

img_opening = cv2.morphologyEx(gray_img, cv2.MORPH_OPEN, kernel)

img_opening = cv2.addWeighted(gray_img, 1, img_opening, -1, 0)

ret,img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

img_edge = cv2.Canny(img_thresh, 100, 200)

kernel = np.ones((10, 10), np.uint8)

img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel)

img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel)

image,contours,hierarchy = cv2.findContours(img_edge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow('img',img)

# cv2.imshow('gray_img', gray_img)

cv2.imshow('ret',img_thresh )

cv2.waitKey(0)

cv2.destroyAllWindows()

