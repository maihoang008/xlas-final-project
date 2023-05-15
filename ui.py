from PyQt6.QtWidgets import QApplication, QSlider, QWidget, QPushButton, QFileDialog, QLabel, QSizePolicy, QComboBox
from PyQt6.QtGui import QPixmap, QIcon
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
        self.k = None
        self.image = None
        self.cimage = None
    

    def initUI(self):
        self.banner_label1 = QLabel(self)
        banner_pixmap = QPixmap("banner1.png")
        self.banner_label1.setPixmap(banner_pixmap)
        self.banner_label1.setFixedSize(1050, 200)
        self.banner_label1.move(0, 0)
        
        self.banner_label2 = QLabel(self)
        banner_pixmap = QPixmap("banner2.png")
        self.banner_label2.setPixmap(banner_pixmap)
        self.banner_label2.setFixedSize(500, 200)
        self.banner_label2.move(1040, 0)

        # File label
        self.file_label = QLabel('', self)
        self.file_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.banner_label1.setScaledContents(True) 
        self.banner_label2.setScaledContents(True) 
        # Image label
        self.image_label = QLabel(self)
        self.image_label.move(5, 210)
        self.image_label.setFixedSize(750, 500)
        self.image_label.setScaledContents(True) 
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Image label
        self.image_label_after = QLabel(self)
        self.image_label_after.move(780, 210)
        self.image_label_after.setFixedSize(750, 500)
        self.image_label_after.setScaledContents(True) 
        self.image_label_after.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Replace Origin and Save As button Layout
        
        self.slider_label = QLabel(self)
        self.slider_label.setFixedSize(60, 50)
        self.slider_label.setScaledContents(True) 
        self.slider_label.move(480, 740)
        
        self.slider = QSlider(Qt.Orientation.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setFixedWidth(250)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setHidden(True)
        self.slider.move(550, 750)
        
        self.replace_button = QPushButton('Replace Origin', self)
        self.replace_button.clicked.connect(self.replace_origin)
        self.replace_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.replace_button.setStyleSheet("background-color: #ffb38a;")
        self.replace_button.move(1300, 750)
        
        self.save_as_button = QPushButton('Save as', self)
        self.save_as_button.clicked.connect(self.save_as)
        self.save_as_button.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.save_as_button.setStyleSheet("background-color: #ffb38a;")
        self.save_as_button.move(1400, 750)
        

        # Add four buttons to the layout
        self.button1 = QPushButton('Browse', self)
        self.button1.clicked.connect(self.showDialog)
        self.button1.setStyleSheet("background-color: #ffb38a;")
        self.button1.move(50, 750)
        
        #Them chuc nang o day
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["","Gaussian", "Max", "Min","Median","Reduce noise","Sharpening","Rotation","grayscale"])
        self.comboBox.activated[int].connect(self.combo)
        self.comboBox.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.comboBox.setStyleSheet("background-color: #ffb38a;")
        self.comboBox.setFixedWidth(200)
        self.comboBox.move(170, 750)
        

        self.slider.valueChanged.connect(self.slide)
        
        
        # Disable the first time user open the app
        self.comboBox.setEnabled(False)
        self.save_as_button.setEnabled(False)
        self.replace_button.setEnabled(False)








        # Set the default image
        self.default_image = os.path.join(os.path.dirname(__file__), 'default.jpg')
        pixmap = QPixmap(self.default_image)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label.height())
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label_after.setPixmap(scaled_pixmap)


        self.setWindowIcon(QIcon('camera.png'))
        self.setStyleSheet("background-color: #ADD8E6 ;")
        self.showMaximized()
        self.setWindowTitle('Final project')
        self.show()
    
    
    def slide(self):
        self.slider_label.setText("Value: "+str(self.sender().value()))
    
    def combo(self):
        self.slider.setValue(0)
        self.slider.setHidden(True)
        if self.comboBox.currentIndex()==1:
            self.slider.setHidden(False)
            self.gaussian_filter()
            self.slider.valueChanged[int].connect(self.gaussian_filter)
        elif self.comboBox.currentIndex()==2:
            self.slider.setHidden(False)
            self.max_filter()
            self.slider.valueChanged[int].connect(self.max_filter)
        elif self.comboBox.currentIndex()==3:
            self.slider.setHidden(False)
            self.min_filter()
            self.slider.valueChanged[int].connect(self.min_filter)
        elif self.comboBox.currentIndex()==4:
            self.slider.setHidden(False)
            self.medianBlur()
            self.slider.valueChanged[int].connect(self.medianBlur)
        elif self.comboBox.currentIndex()==5:
            self.reduce_noise()
        elif self.comboBox.currentIndex()==6:
            self.sharpening()
        elif self.comboBox.currentIndex()==7:
            self.slider.setMaximum(360)
            self.slider.setHidden(False)
            self.rotation()
            self.slider.valueChanged[int].connect(self.rotation)
        elif self.comboBox.currentIndex()==8:
            self.grayscale()
            
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
        self.image =self.cimage
        # Get the pixmap from the image_label_after
        pixmap_after = self.image_label_after.pixmap()

        if pixmap_after:
            # Set the pixmap from the image_label_after to the image_label
            self.image_label.setPixmap(pixmap_after)

            # Set the default image for the image_label_after
            default_pixmap = QPixmap(self.default_image)
            scaled_default_pixmap = default_pixmap.scaledToHeight(self.image_label_after.height())
            self.image_label_after.setPixmap(scaled_default_pixmap)

    def min_filter(self,k=0):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((k, k), np.uint8)
        erosion = cv2.erode(gray, kernel, iterations=1)
        img = cv2.cvtColor(erosion, cv2.COLOR_GRAY2RGB)
        erosion_rgb = cv2.resize(img, (1640, 900))
        qimg = QImage(erosion_rgb.data, erosion_rgb.shape[1], erosion_rgb.shape[0], QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)
        self.cimage  = erosion_rgb

    def max_filter(self,k=0):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((k, k), np.uint8)
        dilation = cv2.dilate(gray, kernel, iterations=1)
        img = cv2.cvtColor(dilation, cv2.COLOR_GRAY2RGB) # Convert to RGB color space
        dilation_rgb = cv2.resize(img, (1640, 900))
        qimg = QImage(dilation_rgb.data, dilation_rgb.shape[1], dilation_rgb.shape[0], QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)
        self.cimage  = dilation_rgb

    
    def gaussian_filter(self,k=1):
        if k%2==0:
            k+=1
        img = cv2.GaussianBlur(self.image, (k, k), 0)
        gaussian = cv2.resize(img, (1640, 900))
        qimg = QImage(gaussian.data, gaussian.shape[1], gaussian.shape[0], QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)
        self.image_label_after.adjustSize()
        self.cimage  = gaussian
 
    def medianBlur(self,k=1):
        if k%2==0:
            k+=1
        img=cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        img = cv2.medianBlur(img,k)
        
        image = cv2.resize(img, (1640, 900))
        qimg = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)
        self.image_label_after.adjustSize()
        self.cimage  = image
        
    def reduce_noise(self):
        detect = cv2.fastNlMeansDenoisingColored(self.image,None,20,10,7,21)
        
        image = cv2.resize(detect, (1640, 900))
        qimg = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)
        self.image_label_after.adjustSize()
        self.cimage  = image
        
    def sharpening(self):
        kernel_sharpening = np.array([[-1,-1,-1], 
                              [-1,9,-1], 
                              [-1,-1,-1]])
        sharpened = cv2.filter2D(self.image, -1, kernel_sharpening)
        image = cv2.resize(sharpened, (1640, 900))
        qimg = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)
        self.image_label_after.adjustSize()
        self.cimage  = image
        
    def rotation(self,k=0):
        rows,cols = self.image.shape[:2] 
        M = cv2.getRotationMatrix2D((cols/2,rows/2),k,1) 
        dst = cv2.warpAffine(self.image,M,(cols,rows))
        image = cv2.resize(dst, (1640, 900))
        qimg = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_BGR888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap) 
        self.image_label_after.adjustSize()
        self.cimage  = image
    
    def grayscale(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(gray, (1640, 900))
        qimg = QImage(image.data, image.shape[1], image.shape[0], QImage.Format.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label_after.height())
        self.image_label_after.setPixmap(scaled_pixmap)
        self.cimage  = image
        

    def showDialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/Users/asus/OneDrive/Pictures', 'Images (*.png *.jpg)')
        if fname:
            self.image_path = fname
            self.image = cv2.imread(self.image_path)
            pixmap = QPixmap(fname)
            scaled_pixmap = pixmap.scaledToHeight(self.image_label.height())
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label_after.setPixmap(scaled_pixmap)

            # Enable back buttons
            self.comboBox.setEnabled(True)
            self.save_as_button.setEnabled(True)
            self.replace_button.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_browser = FileBrowser()
    sys.exit(app.exec())