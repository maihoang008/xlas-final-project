from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt6.QtGui import QPixmap, QTransform, QIcon
from PyQt6.QtCore import Qt
import sys, os

class FileBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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
        button3 = QPushButton('Max', self)
        button4 = QPushButton('Min', self)

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

    def showDialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Images (*.png *.jpg)')
        if fname:
            pixmap = QPixmap(fname)
            scaled_pixmap = pixmap.scaledToHeight(self.image_label.height())
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label_after.setPixmap(scaled_pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_browser = FileBrowser()
    sys.exit(app.exec())
