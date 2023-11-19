import sys
import socket
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
import qrcode

class ServerControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.client_process = None
        self.server_process = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('가상 조이콘 연결')
        self.setGeometry(100, 100, 500, 200)

        # 서버 시작 버튼 생성 및 클릭 이벤트 연결
        self.startButton = QPushButton('통신 서버 시작', self)
        self.startButton.setStyleSheet("background-color: #02bbde; padding: 20px; color: white; border-radius: 10px;")
        self.startButton.clicked.connect(self.startServer)

        # 프로세스 및 GUI 종료 버튼 생성 및 클릭 이벤트 연결
        self.exitButton = QPushButton('종료', self)
        self.exitButton.setStyleSheet("background-color: #ff5e52; padding: 20px; color: white; border-radius: 10px;")
        self.exitButton.clicked.connect(self.exitApp)

        # 이미지 뷰어 라벨 생성
        self.qrLabel = QLabel(self)

        self.helpLabel = QLabel(self)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.startButton)
        layout.addWidget(self.exitButton)
        layout.addWidget(self.qrLabel)
        layout.addWidget(self.helpLabel)
        self.setLayout(layout)

        self.show()

    def startServer(self):
        # 명령어 실행 및 프로세스 저장
        self.client_process = subprocess.Popen(["python", "client.py"], shell=True)
        web_directory = "C:\Users\icecr/Desktop/joycon/web" # 실행하는 PC에 맞게 경로 수정
        self.server_process = subprocess.Popen(["python", "-m", "http.server", "3000"], shell=True, cwd=web_directory)
        QMessageBox.information(self, "서버 시작", "서버가 시작되었습니다.")

        # 현재 PC의 IP 주소 얻기
        ip_address = socket.gethostbyname(socket.gethostname())

        # QR 코드 생성 및 표시
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=15,
            border=4
        )
        qr.add_data(f'http://{ip_address}:3000/v2')
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("qr_code.png")

        # 이미지 뷰어에 QR 코드 표시
        pixmap = QPixmap("qr_code.png")
        self.qrLabel.setPixmap(pixmap)
        self.qrLabel.resize(pixmap.width(), pixmap.height())
        self.helpLabel.setText("      스마트폰으로 QR 코드를 스캔하세요")

    def exitApp(self):
        # 실행 중인 서버 프로세스 종료
        if self.client_process:
            self.client_process.terminate()
            self.client_process.wait()
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()

        # GUI 종료
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ServerControlApp()
    sys.exit(app.exec_())