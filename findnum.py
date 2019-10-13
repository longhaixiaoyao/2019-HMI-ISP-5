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


def predict(imageArr):
    img_copy = imageArr.copy()
    gray_img = cv2.cvtColor(img_copy , cv2.COLOR_BGR2GRAY)
    gray_img_ = cv2.GaussianBlur(gray_img, (5,5), 0, 0, cv2.BORDER_DEFAULT)
    kernel = np.ones((23, 23), np.uint8)
    img_opening = cv2.morphologyEx(gray_img, cv2.MORPH_OPEN, kernel)
    img_opening = cv2.addWeighted(gray_img, 1, img_opening, -1, 0)
    # 找到图像边缘
    ret,img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img_edge = cv2.Canny(img_thresh, 100, 200)
    # # 使用开运算和闭运算让图像边缘成为一个整体
    kernel = np.ones((10, 10), np.uint8)
    img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel)
    img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel)
    # # 查找图像边缘整体形成的矩形区域，可能有很多，车牌就在其中一个矩形区域中
    image,contours,hierarchy = cv2.findContours(img_edge2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return gray_img_,contours,img_edge2


def  chose_licence_plate(contours,Min_Area = 2000):
    temp_contours = []
    for contour in contours:
        if cv2.contourArea( contour ) > Min_Area:
            temp_contours.append(contour)
    car_plate = []
    for temp_contour in temp_contours:
        rect_tupple = cv2.minAreaRect( temp_contour )
        rect_width, rect_height = rect_tupple[1]
        if rect_width < rect_height:
            rect_width, rect_height = rect_height, rect_width
        aspect_ratio = rect_width / rect_height
        # 车牌正常情况下宽高比在2 - 5.5之间
        if aspect_ratio > 2 and aspect_ratio < 3.5:
            car_plate.append( temp_contour )
            rect_vertices = cv2.boxPoints( rect_tupple )
            rect_vertices = np.int0( rect_vertices )
    return  car_plate


def license_segment( car_plates ):
    if len(car_plates)==1:
        for car_plate in car_plates:
            row_min,col_min = np.min(car_plate[:,0,:],axis=0)
            row_max, col_max = np.max(car_plate[:, 0, :], axis=0)
            cv2.rectangle(img, (row_min,col_min), (row_max, col_max), (0,255,0), 2)
            card_img = img[col_min:col_max,row_min:row_max,:]
            cv2.imshow("img", img)
        cv2.imwrite( "card_img.jpg", card_img)
        cv2.imshow("card_img.jpg", card_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return  "card_img.jpg"


img = imread_photo("C:\\Users\\Samson\\Desktop\\coornum.jpg")

#gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

resimg = resize_photo(img)

preimg = predict(resimg)

choseimg = chose_licence_plate(preimg[1])

finalimg = license_segment(car_plates)

cv2.imshow('img',img)

# cv2.imshow('gray_img', gray_img)

cv2.imshow('resimg',resimg)

cv2.imshow('preimg',preimg[2])

cv2.waitKey(0)

cv2.destroyAllWindows()

