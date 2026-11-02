# 🎨 Virtual Air Painting Using Hand Gestures

## 📌 Project Overview

Virtual Air Painting is a computer vision application that allows users to draw on a digital canvas using hand gestures captured through a webcam. It uses Python, OpenCV, NumPy, and cvzone to detect hand movements and create drawings without touching the screen.

## ✨ Features

- **Air Drawing:** Draw on the screen by moving your index finger in the air.
- **Multiple Colors:** Choose from blue, green, red, yellow, and white.
- **Gesture-Based Selection:** Use your index and middle fingers together to select toolbar options.
- **Eraser:** Remove unwanted strokes using hand gestures.
- **Clear Canvas:** Clear the entire drawing with a gesture or keyboard shortcut.
- **Adjustable Brush Size:** Increase or decrease the brush thickness.
- **Save Artwork:** Save drawings as PNG images.
- **Real-Time Hand Tracking:** Track hand movements through a webcam.

## 🛠️ Technologies Used

- Python
- OpenCV
- cvzone
- MediaPipe
- NumPy

## 💻 Requirements

- Python 3.13
- A working webcam
- VS Code or another Python editor
- Required Python libraries

## ⚙️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR-USERNAME/Virtual-Air-Painting.git
```

Replace `YOUR-USERNAME` with your GitHub username.

**2. Open the project folder**

```bash
cd Virtual-Air-Painting
```

**3. Install the dependencies**

```bash
python -m pip install opencv-python numpy cvzone mediapipe
```

**4. Run the application**

```bash
python virtual_painting.py
```

Allow webcam access if prompted.

## 🖐️ Hand Gesture Controls

| Gesture | Action |
|---|---|
| Raise index finger | Draw on the canvas |
| Raise index and middle fingers | Select a toolbar option |
| Select a color | Change the drawing color |
| Select ERASER | Erase unwanted strokes |
| Select CLEAR | Clear the canvas |

## ⌨️ Keyboard Shortcuts

| Key | Function |
|---|---|
| `B` | Switch to brush |
| `E` | Switch to eraser |
| `+` | Increase brush size |
| `-` | Decrease brush size |
| `S` | Save artwork |
| `C` | Clear canvas |
| `Q` or `Esc` | Exit application |

## 💾 Output

The application saves drawings as PNG files inside the `drawings` folder. The folder is created automatically when the application starts.

## 🚀 Future Enhancements

- Add more colors and brush styles.
- Support additional hand gestures.
- Improve the graphical user interface.
- Add undo and redo functionality.
- Add a separate canvas background option.

## 🎯 Conclusion

This project demonstrates how computer vision and hand tracking can be used to create a touch-free digital painting application. It provides an interactive way to draw using natural hand movements.

## 👩‍💻 Author

**Bevara Neeraja**

GitHub: https://github.com/YOUR-USERNAME

---

*Developed as a Python computer vision project.*
