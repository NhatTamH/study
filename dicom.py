import cv2
import pydicom
import numpy as np

# Đường dẫn tới tệp DICOM
file_path = "tumor/style1.dcm"

# Đọc tệp DICOM
dicom_data = pydicom.dcmread(file_path)

# Lấy thông tin về Window Width (WW) và Window Level (WL)
ww = dicom_data.WindowWidth
wl = dicom_data.WindowCenter

# Chuyển đổi dữ liệu DICOM thành mảng numpy
pixel_array = dicom_data.pixel_array

# Áp dụng quá trình chuyển đổi dãy màu
min_value = wl - ww // 2
max_value = wl + ww // 2
clipped_array = np.clip(pixel_array, min_value, max_value)
scaled_array = (clipped_array - min_value) / (max_value - min_value) * 255
image_rgb = cv2.cvtColor(scaled_array.astype(np.uint8), cv2.COLOR_GRAY2RGB)


pixel_array = dicom_data.pixel_array  # Mảng pixel của ảnh DICOM
patient_name = dicom_data.PatientName  # Tên của bệnh nhân trong DICOM

if 'SliceThickness' in dicom_data:
    slice_thickness = dicom_data.SliceThickness
    # print("Độ dày lát cắt: ", slice_thickness)

if 'PixelSpacing' in dicom_data:
    pixel_spacing = dicom_data.PixelSpacing
    # print("Khoảng cách giữa các điểm ảnh: ", pixel_spacing)
    
# print("Họ và tên người bệnh:", dicom_data.PatientName)
# print("Mã số bệnh nhân:", dicom_data.PatientID)

# Trích xuất dữ liệu pixel
pixel_array = dicom_data.pixel_array

# Hiển thị ảnh sử dụng OpenCV
# cv2.imshow('DICOM Image', image_rgb)
cv2.imwrite("./5.jpg",image_rgb)
cv2.waitKey(0)
cv2.destroyAllWindows()
