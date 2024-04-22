import requests
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox
)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_widget = QWidget(self)
        self.setWindowTitle("Rice Leaf Disease Detection")
        self.resize(360, 640)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMaximumSize(500, 500)
        file_hbox = QHBoxLayout()
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("Select an image file")
        self.file_edit.setReadOnly(True)
        file_hbox.addWidget(self.file_edit)
        file_button = QPushButton("Browse")
        file_button.setStyleSheet("background-color: sandybrown; color: white;")
        file_button.clicked.connect(self.select_file)
        file_hbox.addWidget(file_button)
        predict_button = QPushButton("Predict")
        predict_button.setStyleSheet(
            "background-color: darkblue; color: #FFFFFF; font-size: 14px; font-weight: bold; font-style: italic;"
        )
        predict_button.setMaximumWidth(120)
        predict_button.setFixedHeight(30)
        predict_button.setFixedWidth(100)
        predict_button.clicked.connect(self.predict)
        self.output_label = QLabel(self)
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setStyleSheet("font-weight: bold; font-size: 15px;")
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(file_hbox)
        main_layout.addWidget(predict_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.output_label)
        main_widget.setLayout(main_layout)
        self.setStyleSheet("border-image: url('background.jpg') 20 20 20 20 stretch stretch;")
        self.setCentralWidget(main_widget)
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.file_edit.setText(file_path)
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)

    def predict(self):
        file_path = self.file_edit.text()
        if not file_path:
            QMessageBox.critical(self, "Error", "Please select an image file.")
            return
        try:
            with open(file_path, "rb") as f:
                files = {"file": f}
                response = requests.post("http://localhost:8009/predict", files=files)
                data = response.json()
                predicted_class = data["class"]
                confidence = data["confidence"]
                self.output_label.setText(f"Class: {predicted_class}\nConfidence: {confidence*100}%")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
if __name__ == "__main__":
    app = QApplication([])
    dialog = MainWindow()
    dialog.show()
    app.exec_()