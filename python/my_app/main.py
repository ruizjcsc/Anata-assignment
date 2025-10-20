import sys
import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from paramiko import SSHClient,AutoAddPolicy

image_directory = './img'

# inherits from QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # sets title of application
        self.setWindowTitle("Docker Image Container")

        # sets position and dimensions of application (x, y, width, height)
        self.setGeometry(50, 100, 700, 500)

        self.setAcceptDrops(True)
        
        self.local_images = []
        self.initUI()

    def initUI(self):
        # best practice is to create a central widget where all other widgets live and layouts can be applied
        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        # TITLE LABEL
        self.label = QLabel("Drag Image Here",self)
        self.label.setFont(QFont("Arial",40))
        # uses css type style sheet
        self.label.setStyleSheet("border: 4px dashed white;")
        # sets alignment 
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # UPLOAD BUTTON
        self.button_u = QPushButton("Upload Image",self)
        self.button_u.setFixedSize(250,80)
        self.button_u.clicked.connect(self.uploadImg)

        # DOWNLOAD BUTTON
        self.button_d = QPushButton("Download Latest Image",self)
        self.button_d.setFixedSize(250,80)
        self.button_d.clicked.connect(self.downloadImg)

        # LAYOUT
        vBox = QVBoxLayout()
        vBox.addWidget(self.label)
        vBox.addWidget(self.button_u)
        vBox.addWidget(self.button_d)
        # grid.addWidget(imageLabel,2,0)


        central_widget.setLayout(vBox)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            pixmap = QPixmap(event.mimeData().urls()[0].toLocalFile())
            self.label.setPixmap(pixmap)
            self.local_images.append(event.mimeData().urls()[0].toLocalFile())
            print(self.local_images)
            event.acceptProposedAction()
            
    def uploadImg(self):
        client = SSHClient()
        # if host is unknow it fails by default, this auto adds unkown hosts to known hosts
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname='localhost', port=2222, username='root',key_filename='/Users/jonathanr/Docker/Anata_assignment/docker_access')

        sftp_client = client.open_sftp()

        local_image_name = os.path.basename(self.local_images[0])

        sftp_client.put(localpath=self.local_images[0], remotepath=f'/app/images/{local_image_name}')

        stdin, stdout, stderr = client.exec_command('ls -l /app/images')
        print(stdout.read().decode())

        sftp_client.close()
        client.close()

    def downloadImg(self):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname='localhost', port=2222, username='root',key_filename='/Users/jonathanr/Docker/Anata_assignment/docker_access')

        sftp_client = client.open_sftp()

        images = self.remote_images()

        remotePath = f'/app/images/{images[-1]}'

        sftp_client.get(remotepath=remotePath, localpath=f'./img/{images[-1]}')

        stdin, stdout, stderr = client.exec_command('ls -l /app/images')
        print(stdout.read().decode())


        self.label.setPixmap(QPixmap(f'./img/{images[-1]}'))
        

        sftp_client.close()
        client.close()
    
    def remote_images(self):
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect(hostname='localhost', port=2222, username='root',key_filename='/Users/jonathanr/Docker/Anata_assignment/docker_access')

        stdin, stdout, stderr = client.exec_command('ls /app/images')
        filenames = "".join(stdout.read().decode()).strip().split("\n")
        print(filenames)
        return filenames


def main():
    # allows pyqt to use command line arugments
    app = QApplication(sys.argv)

    # gets your window class
    window = MainWindow()

    # use show method to show application window
    window.show()

    # exit condition so that it doesnt close till user closes window manuall
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
