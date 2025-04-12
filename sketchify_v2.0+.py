import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QCheckBox, QFrame, QSlider
from PyQt6.QtGui import QPixmap, QImage, QIcon
from PyQt6.QtCore import Qt
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class SketchifyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sketchify - AI Image to Sketch Generator")
        self.setGeometry(100, 100, 1200, 700)
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        self.initUI()

        self.cv_image = None
        self.sketch_image = None  # Store the generated sketch image
        self.original_image = None

        self.setWindowIcon(QIcon(r"C:\Users\JATOTHU ANAND\Desktop\MY PC\My World\code\logo.png"))

    def initUI(self):
        main_layout = QVBoxLayout()

        # Image Display Area
        image_box_layout = QHBoxLayout()
        self.original_label = QLabel("Original Image")
        self.original_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_label.setFixedSize(400, 400)
        self.original_label.setFrameShape(QFrame.Shape.Box)
        image_box_layout.addWidget(self.original_label)

        self.image_label = QLabel("Sketch Output")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(400, 400)
        self.image_label.setFrameShape(QFrame.Shape.Box)
        image_box_layout.addWidget(self.image_label)

        main_layout.addLayout(image_box_layout)

        # Mode & Controls
        control_layout = QHBoxLayout()

        self.mode_selector = QComboBox()

        # Updated mode list
        self.mode_selector.addItems(["Pencil Sketch", "Drawing Mode"])

        self.mode_selector.currentIndexChanged.connect(self.update_sketch)
        control_layout.addWidget(self.mode_selector)

        self.threshold_slider = QSlider(Qt.Orientation.Horizontal)
        self.threshold_slider.setMinimum(10)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setValue(100)
        self.threshold_slider.valueChanged.connect(self.update_sketch)
        control_layout.addWidget(self.threshold_slider)

        self.gpu_check = QCheckBox("Enable GPU Acceleration")
        self.gpu_check.setStyleSheet("color: white;")
        control_layout.addWidget(self.gpu_check)

        main_layout.addLayout(control_layout)

        # Buttons (Bottom)
        button_layout = QHBoxLayout()

        def create_button(text, func):
            btn = QPushButton(text)
            btn.setFixedSize(120, 30)
            btn.clicked.connect(func)
            return btn

        button_layout.addWidget(create_button("Load Image", self.load_image))
        button_layout.addWidget(create_button("Save Sketch", self.save_sketch))
        button_layout.addWidget(create_button("Undo", self.undo))
        button_layout.addWidget(create_button("Redo", self.redo))

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.jpg *.bmp)")
        if file_path:
            self.cv_image = cv2.imread(file_path)
            self.original_image = self.cv_image.copy()
            self.display_image(self.original_image, self.original_label)
            self.update_sketch()

    def save_sketch(self):
        if self.sketch_image is None:
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Sketch", "", "Images (*.png *.jpg)")
        if file_path:
            cv2.imwrite(file_path, self.sketch_image) 

    def undo(self):
        if self.original_image is not None:
            self.cv_image = self.original_image.copy()
            self.display_image(self.cv_image, self.image_label)

    def redo(self):
        self.update_sketch()

    def update_sketch(self):
        if self.cv_image is None:
            return

        mode = self.mode_selector.currentText()
        threshold = self.threshold_slider.value()
        use_gpu = self.gpu_check.isChecked()

        try:
            if mode == "Pencil Sketch":
                self.sketch_image = self.pencil_sketch(self.cv_image, threshold, use_gpu)
            elif mode == "Drawing Mode":
                self.sketch_image = self.drawing_mode(self.cv_image)
            elif mode == "Double Outline":
                self.sketch_image = self.double_outline(self.cv_image, threshold, use_gpu)

            self.display_image(self.sketch_image, self.image_label)

        except Exception as e:
            print(f"Error: {e}")

    def pencil_sketch(self, image, threshold, use_gpu=False):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        if use_gpu:
            # Using CUDA-enabled OpenCV (if available) for GPU acceleration
            if cv2.cuda.getCudaEnabledDeviceCount() > 0:
                gpu_gray = cv2.cuda_GpuMat()
                gpu_gray.upload(gray)
                gpu_sketch = cv2.cuda.threshold(gpu_gray, threshold, 255, cv2.THRESH_BINARY)[1]
                return gpu_sketch.download()
            else:
                print("GPU not available. Falling back to CPU.")

        # CPU-based pencil sketch (default)
        sketch = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)[1]
        return sketch

    def drawing_mode(self, image):
        # Use OpenCV to save the image temporarily for Drawing Mode
        temp_path = "temp_image.jpg"

        cv2.imwrite(temp_path, image)

        # Function to convert image to sketch (original logic)
        def image_to_sketch(img_path):
            img = cv2.imread(img_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            inverted = cv2.bitwise_not(gray)
            blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
            inverted_blurred = cv2.bitwise_not(blurred)
            sketch = cv2.divide(gray, inverted_blurred, scale=256.0)
            sketch_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)

            return sketch_rgb

        # Convert the image to sketch using Drawing Mode
        sketch = image_to_sketch(temp_path)

        return sketch
    
    def double_outline(self, image, threshold, use_gpu=False):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold, threshold * 2)
        # Inverting the edges to make background white and edges black
        edges_inv = cv2.bitwise_not(edges)
        edges_thick = cv2.dilate(edges_inv, None, iterations=2)

        return edges_thick

    def display_image(self, image, label):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        q_image = QImage(image.data, image.shape[1], image.shape[0], image.shape[1] * 3, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap)
        label.setScaledContents(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SketchifyApp()
    window.show()
    sys.exit(app.exec())