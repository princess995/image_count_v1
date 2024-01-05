import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QFont
from ultralytics import YOLO
import math
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

model = YOLO('best.pt')

def object_count(img):
    results = model.predict(source=img, conf=0.6, save=True)

    tong_count = 0
    cap_count = 0

    for c in results[0].boxes.cls:
        class_idx = int(c)
        if class_idx == 1:
            tong_count += 1
        elif class_idx == 0:
            cap_count += 1

    return tong_count, cap_count


def result_counter(front, side, top):
    result = 0

    front_tong, front_cap = object_count(front)
    side_tong, side_cap = object_count(side)
    top_tong, top_cap = object_count(top)

    
    result = int(math.sqrt(front_tong * side_tong * top_cap))

    return result


class ImageCount(QWidget):
    def __init__(self):
        super().__init__()
        self.image_path1 = None
        self.image_path2 = None
        self.image_path3 = None
        
        self.initUI()
        
    def initUI(self):
        
        
        
        self.setWindowTitle('image_count')
        self.setGeometry(500, 500, 400, 400)
        
        
        
        # 이미지 표시
        icon_path = resource_path('image/icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.display_image()
        
        
        
        
        # 이미지(앞) 불러오기 버튼
        self.select_image_btn = QPushButton('front')
        self.select_image_btn.clicked.connect(lambda: self.select_image('front'))
        
        
        # 이미지(옆) 불러오기 버튼
        self.select_image_btn2 = QPushButton('side')
        self.select_image_btn2.clicked.connect(lambda: self.select_image('side'))
        
        
        # 이미지(위) 불러오기 버튼
        self.select_image_btn3 = QPushButton('top')
        self.select_image_btn3.clicked.connect(lambda: self.select_image('top'))
        
        
        # 이미지 갯수 카운트 버튼
        self.count_btn = QPushButton('count')
        self.count_btn.clicked.connect(self.count)
        
        
        # 결과 표시 레이블
        self.result_label = QLabel('')
        font = QFont()
        font.setPointSize(16)  # 폰트 크기 설정
        font.setBold(True)    # 굵게 설정
        self.result_label.setFont(font)
        self.result_label.setStyleSheet("color: black;")  # 검정색 텍스트
        
        
        
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.select_image_btn)
        layout.addWidget(self.select_image_btn2)
        layout.addWidget(self.select_image_btn3)
        layout.addWidget(self.count_btn)
        layout.addWidget(self.result_label)
        
        
        
        
        
        
        
        self.setLayout(layout)
        
        # self.move_widgets()
        
    def select_image(self, image_type):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp)")
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                if image_type == 'front':
                    self.image_path1 = selected_files[0]
                    self.select_image_btn.setText(f'front-select: {os.path.basename(self.image_path1)}')
                elif image_type == 'side':
                    self.image_path2 = selected_files[0]
                    self.select_image_btn2.setText(f'side-select: {os.path.basename(self.image_path2)}')
                elif image_type == 'top':
                    self.image_path3 = selected_files[0]
                    self.select_image_btn3.setText(f'top-select: {os.path.basename(self.image_path3)}')
            
    def count(self):
        if self.image_path1 and self.image_path2 and self.image_path3:
            count = result_counter(self.image_path1, self.image_path2, self.image_path3)
            self.result_label.setText(f'count: {count}')
        else:
            self.result_label.setText('all select images.')
            
    def display_image(self):
        icon = QLabel(self)
        image_path = resource_path('image/main.png')
        pixmap = QPixmap(image_path)
        icon.setPixmap(pixmap)
        icon.resize(pixmap.width(), pixmap.height())  # 이미지 크기 조정
        icon.move(50, 50)
        

    

    

        


if __name__ == '__main__':
    app = QApplication([])
    window = ImageCount()
    window.show()
    app.exec_()