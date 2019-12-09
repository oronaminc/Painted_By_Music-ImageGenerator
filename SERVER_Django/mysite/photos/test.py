import cv2
import os

pth = os.path.dirname(os.path.dirname(__file__))
path = pth+'/static/images/'
img = cv2.imread('style2.jpg')
row = img.shape[0]
ratio = 148/row
resize_img = cv2.resize(img, dsize=(0,0), fx=ratio, fy=ratio, interpolation=cv2.INTER_AREA)
cv2.imwrite(path +'resize.jpg', resize_img)
cv2.waitKey()