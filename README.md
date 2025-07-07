# 🖱️ Virtual Mouse using MediaPipe & OpenCV

A gesture-controlled virtual mouse system that lets you control your laptop cursor with hand movements using **MediaPipe**, **OpenCV**, and **PyAutoGUI**.

---

## 📌 Features

* 👆 Move cursor by just moving your index finger
* ✌️ Click using finger gestures or colored objects
* 🤖 Real-time hand tracking using **MediaPipe**
* 🎯 Smooth cursor control mapped to screen coordinates
* 💡 Lightweight and runs on CPU (no GPU needed)

---

## 📂 Project Structure

```
VirtualMouse/
├── virtual_mouse.py           # Main script for controlling cursor via gesture
├── requirements.txt           # Required Python libraries
├── README.md                  # Project info and instructions
└── .gitignore                 # Files to be ignored in Git
```

---

## ⚙️ Requirements

* Python 3.7 – 3.10
* OpenCV
* MediaPipe
* NumPy
* PyAutoGUI

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run

```bash
python virtual_mouse.py
```

Then:

* Move your finger to move the cursor
* Use click gesture or specific color (e.g., blue) to perform a click
* Press `q` to exit

---

## 🔧 Enhancements (Coming Soon)

* ✋ Add gesture for **right click** and **drag-drop**
* 🔄 Switch between **MediaPipe** and **Color-based detection** dynamically
* 🧠 Use **AI model** for multi-gesture recognition
* 📸 Add screen recording while using the virtual mouse

---

## 🧠 Learnings

This project helped me understand:

* Real-time computer vision with OpenCV
* Hand landmark detection using MediaPipe
* Mapping frame to screen coordinates
* Controlling OS input with PyAutoGUI

---

## 📸 Demo

*Coming soon – GIF of the working project in action!*

---

## 🤝 Contribution

Feel free to fork the repo and suggest improvements!

---

## 📝 License

MIT License – free to use with attribution.
