# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 04:16:26 2023

@author: quanv
"""

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap, QTransform, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage

import sys, os
import cv2
import numpy as np


class FileBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_path = None


    def initUI(self):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle('File Browser')
        self.setWindowIcon(QIcon('icon.png'))

        # Banner label
        self.banner_label = QLabel(self)
        self.banner_label.setPixmap(QPixmap("banner.png"))
        self.banner_label.setFixedHeight(300)
        self.banner_label.setFixedWidth(self.width())

        # Text label
        self.text_label = QLabel(self)
        self.text_label.setFixedWidth(200)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.text_label.setWordWrap(True)
        self.text_label.setText("Nhóm xx\nNguyễn Mai Hoàng 19110208\nTên ông 1 MSSV_1\nTên ông 2 MSSV_2")

        # Horizontal layout for banner and text
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.banner_label)
        header_layout.addWidget(self.text_label)

        # File label
        self.file_label = QLabel('', self)
        self.file_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.banner_label.setScaledContents(True) # Set scaledContents to True
        self.file_label.setText("Project môn xử lý ảnh số ")

        # Image label
        self.image_label = QLabel(self)
        self.image_label.move(20, 60)
        self.image_label.setFixedWidth(400)
        self.image_label.setFixedHeight(200)
        self.image_label.setText("Choose your image to start")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Image label
        self.image_label_after = QLabel(self)
        self.image_label_after.move(420, 80)
        self.image_label_after.setFixedWidth(400)
        self.image_label_after.setFixedHeight(200)
        self.image_label_after.setText("Choose your image to start")
        self.image_label_after.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout for the file label and buttons
        hbox = QHBoxLayout()
        hbox.addWidget(self.file_label)

        # Add four buttons to the layout
        button1 = QPushButton('Browse', self)
        button1.clicked.connect(self.showDialog)
        button2 = QPushButton('Gaussian', self)
        button2.clicked.connect(self.gaussian_filter)
        button3 = QPushButton('Max', self)
        button3.clicked.connect(self.max_filter)
        button4 = QPushButton('Min', self)
        button4.clicked.connect(self.min_filter)

        button1.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        button2.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        button3.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        button4.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(button1)
        hbox2.addWidget(button2)
        hbox2.addWidget(button3)
        hbox2.addWidget(button4)

        # Create a horizontal layout for the image labels
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.image_label_after)

        # Set the layout for the window
        vbox = QVBoxLayout()
        vbox.addLayout(header_layout) # Add the header layout
        vbox.addLayout(hbox)
        vbox.addLayout(image_layout)
        vbox.addLayout(hbox2)
        vbox.setStretch(0, 1)
        vbox.setStretch(1, 2)
        vbox.setStretch(2, 4)
        vbox.setStretch(3, 4)
        vbox.setStretch(4, 1)
        vbox.setSpacing(20)
        self.setLayout(vbox)

        # Set the default image
        self.default_image = os.path.join(os.path.dirname(__file__), 'default.jpg')
        pixmap = QPixmap(self.default_image)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label.height())
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label_after.setPixmap(scaled_pixmap)
        self.show()
    
    

    def min_filter(self):
        if not self.image_path:
            return
        try:
            image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                return
            kernel = np.ones((5, 5), np.uint8)
            erosion = cv2.erode(image, kernel, iterations=1)
            qimg = QImage(erosion.data, erosion.shape[1], erosion.shape[0], QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
            self.image_label_after.setPixmap(scaled_pixmap)
        except cv2.error as e:
            print(f"Error processing image: {e}")

        
    def max_filter(self):
        if not self.image_path:
            return
        image = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            return
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(image, kernel, iterations=1)
        dilation_rgb = cv2.cvtColor(dilation, cv2.COLOR_GRAY2RGB) # Convert to RGB color space
        qimg = QImage(dilation_rgb.data, dilation_rgb.shape[1], dilation_rgb.shape[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)

    
    def gaussian_filter(self):
        if not self.image_path:
            return
        image = cv2.imread(self.image_path)
        if image is None:
            return
        gaussian = cv2.GaussianBlur(image, (5, 5), 0)
        qimg = QImage(gaussian.data, gaussian.shape[1], gaussian.shape[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)
        self.image_label_after.adjustSize() #Thêm dòng này để hiển thị đúng kích thước ảnh

    
    def show_image_after(self, image):
        if len(image.shape) == 2:  # Grayscale image
            qimage = QImage(image.data, image.shape[1], image.shape[0],QImage.Format.Format_Grayscale8)
        else:  # Color image
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap(qimage)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)
    


    def showDialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Images (*.png *.jpg)')
        if fname:
            self.image_path = fname
            pixmap = QPixmap(fname)
            scaled_pixmap = pixmap.scaledToHeight(self.image_label.height())
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label_after.setPixmap(scaled_pixmap)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_browser = FileBrowser()
    sys.exit(app.exec())
