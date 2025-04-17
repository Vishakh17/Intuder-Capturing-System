![Intruder Capturing System]("C:\Users\Lenovo\OneDrive\Desktop\python\project\intrudercapturingsystem.png")

# Intruder Capturing System

A Python-based security application that monitors login attempts and captures images of unauthorized access. On detecting multiple failed attempts, the system triggers a lockdown and sends an email alert with the intruder's image attached.

---

## 🚀 Features

- User Sign-Up and Login system
- Password validation with lockdown after 3 failed attempts
- Captures image using webcam on failed logins
- Sends Gmail alert with image attachment
- Logs all login attempts with IP address and timestamp
- Login history viewer with reset option
- Graphical dashboard showing success vs failed attempts

---

## 🛠 Technologies Used

- Python 3.x
- Tkinter (GUI)
- OpenCV (Webcam capture)
- smtplib / email.mime (Email alerts)
- PIL (Image preview in GUI)
- Matplotlib (Login statistics chart)

---

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/intruder-capturing-system.git
cd intruder-capturing-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

---

## 🔐 Gmail Setup
To enable email alerts:
1. Use a Gmail account
2. Turn on 2-Step Verification
3. Generate an App Password: https://myaccount.google.com/apppasswords
4. Replace the following lines in the code with your credentials:
```python
self.sender_email = "your_email@gmail.com"
self.sender_password = "your_app_password"
```

---

## 📸 Screenshots (to be added)
- Login interface
- Captured intruder image
- Email alert sample
- Dashboard summary

---

## 📂 Folder Structure
```
project/
├── main.py
├── users.txt
├── intruder_log.txt
├── requirements.txt
├── intruder_capture_<timestamp>.jpg
├── README.md
```

---

## 📦 requirements.txt
```
tk
opencv-python
Pillow
matplotlib
```

---

## 🙋‍♂️ Author
**Vishakh Shetty**  
[GitHub Profile](https://github.com/Vishakh17)  
[LinkedIn](https://www.linkedin.com/in/vishakh-shetty-3b783932b/)

---

## ⭐️ Support
If you find this project useful, give it a ⭐️ on GitHub and share it with others!

