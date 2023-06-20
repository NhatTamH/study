'''
 # @ Author: Your name
 # @ Create Time: 2023-06-13 07:17:05
 # @ Modified by: Your name
 # @ Modified time: 2023-06-13 10:47:51
 # @ Description:
 '''

# from tensorflow.keras.models import load_model
from keras.models import load_model
import cv2 as cv
import imutils

model = load_model('brain_tumor_detector.h5')


def predictTumor(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=2)

    # Find contours in thresholded image, then grab the largest one
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv.contourArea)

    # Find the extreme points
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    
    # crop new image out of the original image using the four extreme points (left, right, top, bottom)
    new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]

    image = cv.resize(new_image, dsize=(240, 240), interpolation=cv.INTER_CUBIC)
    image = image / 255.

    image = image.reshape((1, 240, 240, 3))

    res = model.predict(image)
    print(res,"res")
    # cv.imwrite("1.jpg",res)

    return res

def size(image):
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv.threshold(gray, 45, 255, cv.THRESH_BINARY)[1]
    thresh = cv.erode(thresh, None, iterations=2)
    thresh = cv.dilate(thresh, None, iterations=2)

    # Find contours in thresholded image, then grab the largest one
    cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv.contourArea)

    # Find the extreme points
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    
    widths = abs(extRight[0] - extLeft[0])
    heights = abs(extBot[1] - extTop[1])

    
    # print("Width:", widths)
    # print("Height:", heights)
    
    new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]
    
    thickness = 2  # Độ dày của khung
    color = (0, 0, 255)  # Màu đỏ (BGR format)
    
    scale_factor = 0.55  # Hệ số thu nhỏ (80%)
    new_width = int(widths * scale_factor)
    new_height = int(heights * scale_factor)


    shift_amount = 10  # Khoảng dời sang bên phải

    # Tính toán tọa độ mới của khung
    new_extLeft = extLeft[0] + shift_amount + int((widths - new_width) / 2)
    new_extTop = extTop[1] + shift_amount + int((heights - new_height) / 2)
    new_extRight = new_extLeft + shift_amount + new_width
    new_extBot = new_extTop + new_height


    thickness = 2  # Độ dày của khung
    color = (0, 0, 255)  # Màu đỏ (BGR format)

    # Vẽ khung thu nhỏ
    cv.rectangle(image, (new_extLeft, new_extTop), (new_extRight, new_extBot), color, thickness)


    # cv.rectangle(image, (extLeft[0], extTop[1]), (extRight[0], extBot[1]), color, thickness)
    
    # cv.imshow("Object Detection", image)
    filename = "./out.jpg"
    cv.imwrite(filename, image)
    
    cv.waitKey(0)
    cv.destroyAllWindows()
         
    # return widths,heights,extLeft,extRight,extTop,extBot,new_image
    return widths,heights