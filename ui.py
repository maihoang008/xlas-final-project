from PyQt6.QtWidgets import QApplication, QSlider, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy, QComboBox
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
        

        # Banner label
        self.banner_label = QLabel(self)
        # Load the banner pixmap
        banner_pixmap = QPixmap("banner.png")
        # Scale the banner pixmap to the window's width while maintaining its aspect ratio        
        # Set the scaled banner pixmap to the banner label
        self.banner_label.setPixmap(banner_pixmap)
        # Horizontal layout for banner and text
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.banner_label)

        # File label
        self.file_label = QLabel('', self)
        self.file_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.banner_label.setScaledContents(True) 

        # Image label
        self.image_label = QLabel(self)
        self.image_label.move(20, 60)
        self.image_label.setFixedWidth(600)
        self.image_label.setFixedHeight(300)
        self.image_label.setText("Choose your image to start")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Image label
        self.image_label_after = QLabel(self)
        self.image_label_after.move(420, 80)
        self.image_label_after.setFixedWidth(600)
        self.image_label_after.setFixedHeight(300)
        self.image_label_after.setText("Choose your image to start")
        self.image_label_after.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Layout for the file label and buttons
        hbox = QHBoxLayout()
        hbox.addWidget(self.file_label)

        button_style = """
            QPushButton {
                background-color: white;
                color: black;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
            QPushButton:pressed {
                background-color: #E8E8E8;
            }
            QPushButton:disabled {
                background-color: #D3D3D3;
                color: #A0A0A0;
                border: none;
            }
        """
        # Replace Origin and Save As button Layout
        save_as_layout = QHBoxLayout()
        self.slider_label = QLabel(self)
        
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(5)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.valueChanged.connect(self.slide)
        self.slider.valueChanged.connect(self.combo)
        self.slider.setEnabled(False)
        
        self.replace_button = QPushButton('Replace Origin', self)
        self.replace_button.clicked.connect(self.replace_origin)
        self.replace_button.setStyleSheet(button_style)
        self.replace_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        self.save_as_button = QPushButton('Save as', self)
        self.save_as_button.clicked.connect(self.save_as)
        self.save_as_button.setStyleSheet(button_style)
        self.save_as_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        save_as_layout.addWidget(self.slider_label, alignment=Qt.AlignmentFlag.AlignBottom)
        save_as_layout.addWidget(self.slider, alignment=Qt.AlignmentFlag.AlignCenter)
        save_as_layout.addWidget(self.replace_button)
        save_as_layout.addWidget(self.save_as_button)

        # Add four buttons to the layout
        self.button1 = QPushButton('Browse', self)
        self.button1.clicked.connect(self.showDialog)
        
        #Them chuc nang o day
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Gaussian", "Max", "Min"])
        self.comboBox.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        
        self.submit = QPushButton('Submit', self)
        self.submit.clicked.connect(self.combo)
        self.submit.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        # Disable the first time user open the app
        self.comboBox.setEnabled(False)
        self.submit.setEnabled(False)
        self.save_as_button.setEnabled(False)
        self.replace_button.setEnabled(False)

        # Add a label for Browse layout
        browse_label = QLabel('Step 1: Choose your file', self)
        browse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        browse_label.setStyleSheet("color: white;")
        
        # Layout for the Browse button
        browse_layout = QVBoxLayout()
        browse_layout.addWidget(browse_label)
        browse_layout.addWidget(self.button1)

        # Add a label for Browse layout
        filter_label = QLabel('Step 2: Apply the filter', self)
        filter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        filter_label.setStyleSheet("color: white;")

        # Layout for Gaussian, Max, and Min buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.comboBox)
        button_layout.addWidget(self.submit)
        

        # Layout for filter with label
        filter_layout = QVBoxLayout()
        filter_layout.addWidget(filter_label)
        filter_layout.addLayout(button_layout)

        # Add the Browse layout and the button layout to a horizontal layout
        hbox2 = QHBoxLayout()
        hbox2.addLayout(browse_layout)
        hbox2.addLayout(filter_layout)
        hbox2.addLayout(save_as_layout)
        hbox2.setSpacing(10)

        # Create a horizontal layout for the image labels
        image_layout = QHBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addLayout(save_as_layout)
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



        self.showMaximized()
        self.setWindowTitle('Final project')
        self.show()
    
    
    def slide(self):
        
        self.slider_label.setText("Value: "+str(self.sender().value()))
    
    def combo(self):
        self.slider.setEnabled(True)
        print(self.sender().value())
        if self.comboBox.currentIndex()==0:
            self.gaussian_filter(self.sender().value())
        elif self.comboBox.currentIndex()==1:
            self.max_filter()
        elif self.comboBox.currentIndex()==2:
            self.min_filter()
    
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


    def save_as(self):
        if not self.image_path:
            return

        # Get the pixmap from the image_label_after
        pixmap = self.image_label_after.pixmap()

        if pixmap:
            # Get the new file name
            file_name, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Images (*.png *.jpg *.bmp)")

            if file_name:
                # Save the pixmap to the new file name
                pixmap.save(file_name)


    def replace_origin(self):
        if not self.image_path:
            return

        # Get the pixmap from the image_label_after
        pixmap_after = self.image_label_after.pixmap()

        if pixmap_after:
            # Set the pixmap from the image_label_after to the image_label
            self.image_label.setPixmap(pixmap_after)

            # Set the default image for the image_label_after
            default_pixmap = QPixmap(self.default_image)
            scaled_default_pixmap = default_pixmap.scaledToHeight(self.image_label_after.height())
            self.image_label_after.setPixmap(scaled_default_pixmap)



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

    
    def gaussian_filter(self, k = 5):
        if not self.image_path:
            return
        image = cv2.imread(self.image_path)
        image = cv2.resize(image, (300,300))
        if image is None:
            return
        gaussian = cv2.GaussianBlur(image, (k, k), 0)
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
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/Users/asus/OneDrive/Pictures', 'Images (*.png *.jpg)')
        if fname:
            self.image_path = fname
            pixmap = QPixmap(fname)
            scaled_pixmap = pixmap.scaledToHeight(self.image_label.height())
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label_after.setPixmap(scaled_pixmap)

            # Enable back buttons
            self.comboBox.setEnabled(True)
            self.submit.setEnabled(True)
            self.save_as_button.setEnabled(True)
            self.replace_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_browser = FileBrowser()
    sys.exit(app.exec())