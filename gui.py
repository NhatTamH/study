'''
 # @ Author: Your name
 # @ Create Time: 2023-06-13 07:17:05
 # @ Modified by: Your name
 # @ Modified time: 2023-06-13 08:50:28
 # @ Description:
 '''

'''
 # @ Author: Your name
 # @ Create Time: 2023-06-13 07:17:05
 # @ Modified by: Your name
 # @ Modified time: 2023-06-13 08:50:25
 # @ Description:
 '''

import tkinter
from PIL import Image
from tkinter import filedialog
import cv2 as cv
from frames import *
from displayTumor import *
from predictTumor import *
from dicom import *


class Gui:
    MainWindow = 0
    listOfWinFrame = list()
    FirstFrame = object()
    val = 0
    fileName = 0
    DT = object()

    wHeight = 700
    wWidth = 1180

    def __init__(self):
        global MainWindow
        MainWindow = tkinter.Tk()
        MainWindow.geometry('1200x720')
        MainWindow.resizable(width=False, height=False)

        self.DT = DisplayTumor()

        self.fileName = tkinter.StringVar()

        self.FirstFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, 0, 0)
        # self.FirstFrame.btnView['state'] = 'disable'

        self.listOfWinFrame.append(self.FirstFrame)

        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Brain Tumor Detection", height=1, width=40)
        WindowLabel.place(x=320, y=20)
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))
        
        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Do An Tong Hop", height=1, width=40)
        WindowLabel.place(x=320, y=60)  # Đổi giá trị y thành 70
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))

        WindowLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Huynh Phu Thong", height=1, width=40)
        WindowLabel.place(x=320, y=100)  # Đổi giá trị y thành 100
        WindowLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"))

        self.val = tkinter.IntVar()
        RB1 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="Detect Tumor", variable=self.val,
                                  value=1, command=self.check)
        RB1.place(x=250, y=200)
        # RB2 = tkinter.Radiobutton(self.FirstFrame.getFrames(), text="View Tumor Region",
        #                           variable=self.val, value=2, command=self.check)
        # RB2.place(x=250, y=250)

        browseBtn = tkinter.Button(self.FirstFrame.getFrames(), text="Browse", width=8, command=self.browseWindow)
        # browseBtn.place(x=800, y=550)
        browseBtn.place(x=900, y=600)
        
        self.imageViewer = tkinter.Label(self.FirstFrame.getFrames())
        self.imageViewer.place(x=800, y=150)

        MainWindow.mainloop()

    def getListOfWinFrame(self):
        return self.listOfWinFrame

    def browseWindow(self):
        global mriImage
        FILEOPENOPTIONS = dict(defaultextension='*.*',
                               filetypes=[('jpg', '*.jpg'), ('png', '*.png'), ('jpeg', '*.jpeg'), ('All Files', '*.*')])
        self.fileName = filedialog.askopenfilename(**FILEOPENOPTIONS)
        image = Image.open(self.fileName)
        imageName = str(self.fileName)
        mriImage = cv.imread(imageName, 1)
        self.listOfWinFrame[0].readImage(image)
        self.listOfWinFrame[0].displayImage()
        self.DT.readImage(image)   
        # Reset the displayed images in the frames
        # for i in range(1, len(self.listOfWinFrame)):
        #     self.listOfWinFrame[i].resetImage()

    def check(self):
        global mriImage
        #print(mriImage)
        if (self.val.get() == 1):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)

            res = predictTumor(mriImage)
            
            WindowLabel1 = tkinter.Label(self.FirstFrame.getFrames(), text="Độ dày lát cắt: ")
            WindowLabel1.place(x=20, y=500)
            WindowLabel1.configure(background="White", font=("Comic Sans MS", 12))

            WindowLabel2 = tkinter.Label(self.FirstFrame.getFrames(), text="Khoảng cách giữa các điểm ảnh: ")
            WindowLabel2.place(x=20, y=530)
            WindowLabel2.configure(background="White", font=("Comic Sans MS", 12))

            WindowLabel3 = tkinter.Label(self.FirstFrame.getFrames(), text="Họ và tên người bệnh: ")
            WindowLabel3.place(x=20, y=560)
            WindowLabel3.configure(background="White", font=("Comic Sans MS", 12))

            WindowLabel4 = tkinter.Label(self.FirstFrame.getFrames(), text="Mã số bệnh nhân: ")
            WindowLabel4.place(x=20, y=590)
            WindowLabel4.configure(background="White", font=("Comic Sans MS", 12))

            if 'SliceThickness' in dicom_data:
                slice_thickness = dicom_data.SliceThickness
                slice_thickness_label = tkinter.Label(self.FirstFrame.getFrames(), text=slice_thickness)
                slice_thickness_label.place(x=250, y=500)
                slice_thickness_label.configure(background="White", font=("Comic Sans MS", 12))

            if 'PixelSpacing' in dicom_data:
                pixel_spacing = dicom_data.PixelSpacing
                pixel_spacing_label = tkinter.Label(self.FirstFrame.getFrames(), text=pixel_spacing)
                pixel_spacing_label.place(x=250, y=530)
                pixel_spacing_label.configure(background="White", font=("Comic Sans MS", 12))

            patient_name_label = tkinter.Label(self.FirstFrame.getFrames(), text=dicom_data.PatientName)
            patient_name_label.place(x=250, y=560)
            patient_name_label.configure(background="White", font=("Comic Sans MS", 12))

            patient_id_label = tkinter.Label(self.FirstFrame.getFrames(), text=dicom_data.PatientID)
            patient_id_label.place(x=250, y=590)
            patient_id_label.configure(background="White", font=("Comic Sans MS", 12))
            
            if res > 0.5:
                # resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Tumor Detected", height=1, width=20)
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Phát Hiện Khối U", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="red")
                
                WindowLabel5 = tkinter.Label(self.FirstFrame.getFrames(), text="Kích thước khối u: ")
                WindowLabel5.place(x=20, y=620)
                WindowLabel5.configure(background="White", font=("Comic Sans MS", 12))
                
                # widths,heights,extLeft, extRight, extTop, extBot, new_image = size(mriImage) 
                widths,heights = size(mriImage) 
                
                WindowLabel6 = tkinter.Label(self.FirstFrame.getFrames(), text="{}x{}: ".format(widths, heights))
                WindowLabel6.place(x=250, y=620)
                WindowLabel6.configure(background="White", font=("Comic Sans MS", 12))
                
                size(mriImage)
                image = Image.open("./out.jpg")  # Replace with the path to the predicted image
                image = image.resize((250, 250))  # Adjust the size as needed
                photo = ImageTk.PhotoImage(image)
                self.imageViewer.configure(image=photo)
                self.imageViewer.image = photo
                
            else:
                # resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="No Tumor", height=1, width=20)
                resLabel = tkinter.Label(self.FirstFrame.getFrames(), text="Không Có Khối U", height=1, width=20)
                resLabel.configure(background="White", font=("Comic Sans MS", 16, "bold"), fg="green")

            resLabel.place(x=700, y=450)

        elif (self.val.get() == 2):
            self.listOfWinFrame = 0
            self.listOfWinFrame = list()
            self.listOfWinFrame.append(self.FirstFrame)

            self.listOfWinFrame[0].setCallObject(self.DT)
            self.listOfWinFrame[0].setMethod(self.DT.removeNoise)
            secFrame = Frames(self, MainWindow, self.wWidth, self.wHeight, self.DT.displayTumor, self.DT)

            self.listOfWinFrame.append(secFrame)


            for i in range(len(self.listOfWinFrame)):
                if (i != 0):
                    self.listOfWinFrame[i].hide()
            self.listOfWinFrame[0].unhide()

            # if (len(self.listOfWinFrame) > 1):
            #     self.listOfWinFrame[0].btnView['state'] = 'active'

        else:
            print("Not Working")

mainObj = Gui()