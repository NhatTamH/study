import cv2
import imutils
import numpy as np

from tensorflow import keras

model = keras.models.load_model("./brain_tumor_detector.h5")

image = cv2.imread("tumor.jpg")

# Resize ảnh đến kích thước mong muốn
input_shape = (240, 240)
resized_image = cv2.resize(image, input_shape)

# Chuẩn hóa và mở rộng kích thước ảnh đến định dạng input của mô hình YOLO
input_image = np.expand_dims(resized_image, axis=0)
input_image = input_image / 255.0

# Dự đoán đối tượng sử dụng mô hình YOLO
output = model.predict(input_image)
print(output)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Threshold the image, then perform a series of erosions +
# dilations to remove any small regions of noise
thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
thresh = cv2.erode(thresh, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)

# Find contours in thresholded image, then grab the largest one
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)

# Find the extreme points
extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])


# Tính toán kích thước mới của khung
width = extRight[0] - extLeft[0]
height = extBot[1] - extTop[1]
scale_factor = 0.55  # Hệ số thu nhỏ (80%)
new_width = int(width * scale_factor)
new_height = int(height * scale_factor)


shift_amount = 10  # Khoảng dời sang bên phải

# Tính toán tọa độ mới của khung
new_extLeft = extLeft[0] + shift_amount + int((width - new_width) / 2)
new_extTop = extTop[1] + shift_amount + int((height - new_height) / 2)
new_extRight = new_extLeft + shift_amount + new_width
new_extBot = new_extTop + new_height


thickness = 2  # Độ dày của khung
color = (0, 0, 255)  # Màu đỏ (BGR format)

# Vẽ khung thu nhỏ
cv2.rectangle(image, (new_extLeft, new_extTop), (new_extRight, new_extBot), color, thickness)

# Hiển thị ảnh kết quả
# cv2.imshow("Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

