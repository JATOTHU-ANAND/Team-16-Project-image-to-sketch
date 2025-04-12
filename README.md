# Team-16-Project-image-to-sketch
# 🎨 Sketchify - AI Image to Sketch Generator

**Sketchify** is a desktop application built using **PyQt6** and **OpenCV**, allowing you to convert any image into a pencil sketch or a drawing-style sketch with just one click! It features GPU acceleration, threshold control, and multiple sketch modes.

---

## ✨ Features

- 🖼 Load and preview any image
- ✏️ Convert to **Pencil Sketch** or **Drawing Mode**
- 🧠 GPU Acceleration (if supported)
- 🎛 Adjustable sketch threshold
- 💾 Save your sketch output
- 🔁 Undo/Redo support

---

## 📦 Requirements

Install the required dependencies using:

```bash
pip install -r Requirements.txt
If you don't have a requirements.txt, here's the list:

pip install PyQt6 opencv-python numpy Pillow
Note: tkinter is part of the Python standard library, no need to install it separately (make sure it's enabled in your Python installation).

🚀 How to Run
Clone the repository:

git clone https://github.com/your-username/sketchify.git
cd sketchify
Install dependencies:

pip install -r requirements.txt
Run the application:

python sketchify.py
🖥️ Screenshots
Original Image	Sketch Output
🧠 GPU Acceleration (Optional)
If you have a CUDA-enabled GPU, Sketchify can take advantage of it for faster image processing using OpenCV's CUDA modules. This is automatically detected.

Note: The default OpenCV (opencv-python) from pip does not support CUDA. You must build OpenCV from source with CUDA support if needed.

🛠 Future Improvements
Add more sketch filters (e.g., charcoal, ink)

Enable drag and drop support

Add real-time preview slider

Create a cross-platform installer

📜 License
MIT License. Feel free to use, modify, and distribute with credits.

🙌 Acknowledgements
OpenCV

PyQt6

NumPy

Pillow (PIL)
