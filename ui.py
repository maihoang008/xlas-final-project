from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap, QTransform
import sys, os

class FileBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('File Browser')

        # Browse button
        self.button = QPushButton('Browse', self)
        self.button.move(20, 20)
        self.button.clicked.connect(self.showDialog)

        # File label
        self.file_label = QLabel('', self)
        self.file_label.move(130, 25)
        self.file_label.setFixedWidth(300)
        self.file_label.setText("No file chosen")

        # Image label
        self.image_label = QLabel(self)
        self.image_label.move(20, 60)
        self.image_label.setFixedWidth(400)
        self.image_label.setFixedHeight(200)
        self.image_label.setText("Choose your image to start")

        # Image label
        self.image_label_after = QLabel(self)
        self.image_label_after.move(420, 80)
        self.image_label_after.setFixedWidth(400)
        self.image_label_after.setFixedHeight(200)
        self.image_label_after.setText("Choose your image to start")

        # Layout for the file label and buttons
        hbox = QHBoxLayout()
        hbox.addWidget(self.file_label)
        
        # Add four buttons to the layout
        button1 = QPushButton('Median', self)
        hbox.addWidget(button1)
        button2 = QPushButton('Gaussian', self)
        hbox.addWidget(button2)
        button3 = QPushButton('Max', self)
        hbox.addWidget(button3)
        button4 = QPushButton('Min', self)
        hbox.addWidget(button4)

        # Set the layout for the window
        vbox = QVBoxLayout()
        vbox.addWidget(self.button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.image_label)
        self.setLayout(vbox)

        # Set the default image
        self.default_image = os.path.join(os.path.dirname(__file__), 'default.jpg')
        pixmap = QPixmap(self.default_image)
        scaled_pixmap = pixmap.scaledToHeight(self.image_label.height())
        self.image_label.setPixmap(scaled_pixmap)

        self.show()

    def showDialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home', 'Images (*.png *.jpg)')
        if fname:
            pixmap = QPixmap(fname)
            scaled_pixmap = pixmap.scaledToHeight(self.image_label.height())
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label_after.setPixmap(scaled_pixmap)
            self.file_label.setText(fname)
            self.file_label.adjustSize()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    file_browser = FileBrowser()
    sys.exit(app.exec())
