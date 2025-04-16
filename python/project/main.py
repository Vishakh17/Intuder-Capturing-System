import cv2
import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import os
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class IntruderCapturer:
    def __init__(self, master):
        self.master = master
        master.title("Intruder Capturer")
        master.configure(bg='black')

        self.label = tk.Label(master, text="Intruder Capturer", font=("Arial", 16), fg='white', bg='black')
        self.label.pack(pady=10)

        self.status_label = tk.Label(master, text="", font=("Arial", 12), fg='green', bg='black')
        self.status_label.pack(pady=5)

        self.start_button = tk.Button(master, text="Login", command=self.login_prompt,
                                      font=("Arial", 12), bg='red', fg='white')
        self.start_button.pack(pady=10)

        self.signup_button = tk.Button(master, text="Sign Up", command=self.signup_prompt,
                                       font=("Arial", 12), bg='gray', fg='white')
        self.signup_button.pack(pady=10)

        self.history_button = tk.Button(master, text="View Login History", command=self.view_login_history,
                                        font=("Arial", 12), bg='gray', fg='white')
        self.history_button.pack(pady=10)

        self.dashboard_button = tk.Button(master, text="View Dashboard", command=self.view_dashboard,
                                          font=("Arial", 12), bg='blue', fg='white')
        self.dashboard_button.pack(pady=10)

        self.store_dir = r"C:\\Users\\Lenovo\\Downloads\\py1"
        os.makedirs(self.store_dir, exist_ok=True)
        self.log_file = os.path.join(self.store_dir, "intruder_log.txt")
        with open(self.log_file, "a") as log:
            log.write("Log started: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")

        self.users_file = os.path.join(self.store_dir, "users.txt")
        if not os.path.exists(self.users_file):
            open(self.users_file, 'w').close()

        self.current_user_email = None
        self.wrong_attempts = 0
        self.lockdown_until = 0

        self.sender_email = "vishakhshetty310@gmail.com"
        self.sender_password = "bltf anok arvk hxih"
        self.latest_capture_path = None

    def get_ip_address(self):
        return socket.gethostbyname(socket.gethostname())

    def signup_prompt(self):
        email = simpledialog.askstring("Sign Up", "Enter your email:")
        password = simpledialog.askstring("Sign Up", "Set your password:")
        if email and password:
            with open(self.users_file, "a") as f:
                f.write(f"{email},{password}\n")
            messagebox.showinfo("Success", "Account created successfully.")

    def login_prompt(self):
        if time.time() < self.lockdown_until:
            remaining = int(self.lockdown_until - time.time())
            self.status_label.config(text=f"Locked. Try after {remaining}s", fg='yellow')
            return

        email = simpledialog.askstring("Login", "Enter email:")
        password = simpledialog.askstring("Login", "Enter password:")

        if email and password:
            found = False
            with open(self.users_file, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) != 2:
                        continue
                    stored_email, stored_password = parts
                    if email == stored_email:
                        found = True
                        if password == stored_password:
                            self.current_user_email = stored_email
                            self.status_label.config(text="Login successful", fg='green')
                            self.capture_image("Correct password entered")
                            self.wrong_attempts = 0
                        else:
                            self.wrong_attempts += 1
                            self.status_label.config(text=f"Wrong password! Attempt {self.wrong_attempts}/3", fg='red')
                            if self.wrong_attempts >= 3:
                                self.capture_image("Wrong password entered 3 times")
                                self.send_email_alert(stored_email)
                                self.status_label.config(text="Lockdown for 60s", fg='orange')
                                self.lockdown_until = time.time() + 60
                                self.wrong_attempts = 0
                        break
            if not found:
                messagebox.showerror("Error", "Email not found. Please sign up.")

    def send_email_alert(self, recipient_email):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = "Intruder Alert: Failed Login Detected"
            body = f"3 failed login attempts on your account ({recipient_email}) at {time.strftime('%Y-%m-%d %H:%M:%S')}."
            msg.attach(MIMEText(body, 'plain'))

            if self.latest_capture_path:
                with open(self.latest_capture_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(self.latest_capture_path)}"')
                    msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email with attachment sent to {recipient_email}")
        except Exception as e:
            print("❌ Email send failed:", e)

    def capture_image(self, reason):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        ip_address = self.get_ip_address()

        if ret:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            image_path = os.path.join(self.store_dir, f"intruder_capture_{timestamp}.jpg")
            cv2.imwrite(image_path, frame)
            self.latest_capture_path = image_path

            with open(self.log_file, "a") as log:
                log.write(f"{reason}: {time.strftime('%Y-%m-%d %H:%M:%S')} - "
                          f"Saved at {image_path} from IP: {ip_address}\n")
        else:
            messagebox.showerror("Error", "Camera failed.")
        cap.release()

    def view_login_history(self):
        history_window = tk.Toplevel(self.master)
        history_window.title("Login History")
        history_window.configure(bg='black')

        text = tk.Text(history_window, width=60, height=20, bg='black', fg='white', font=("Arial", 12))
        text.pack(padx=10, pady=10)

        reset_btn = tk.Button(history_window, text="Reset History", command=self.reset_login_history,
                              font=("Arial", 12), bg='gray', fg='white')
        reset_btn.pack(pady=10)

        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as log:
                text.insert(tk.END, log.read())

        text.config(state=tk.DISABLED)

    def reset_login_history(self):
        if messagebox.askyesno("Confirm", "Reset login history?"):
            with open(self.log_file, "w") as log:
                log.write("Log started: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            messagebox.showinfo("Reset", "Login history reset.")

    def view_dashboard(self):
        dashboard = tk.Toplevel(self.master)
        dashboard.title("Dashboard")
        dashboard.configure(bg='black')

        tk.Label(dashboard, text="Intruder Dashboard", font=("Arial", 16), fg='white', bg='black').pack(pady=10)

        total = success = fail = 0
        last_time = "N/A"

        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as log:
                lines = log.readlines()
                total = len([l for l in lines if "entered" in l])
                success = len([l for l in lines if "Correct" in l])
                fail = len([l for l in lines if "Wrong" in l])
                for l in reversed(lines):
                    if "entered" in l:
                        last_time = l.split(": ")[1].split(" - ")[0]
                        break

        stats = f"Total: {total}\nSuccess: {success}\nFailed: {fail}\nLast Attempt: {last_time}"
        tk.Label(dashboard, text=stats, font=("Arial", 12), fg='white', bg='black').pack(pady=5)

        latest_img = None
        imgs = [f for f in os.listdir(self.store_dir) if f.endswith(".jpg")]
        if imgs:
            imgs.sort(reverse=True)
            path = os.path.join(self.store_dir, imgs[0])
            img = Image.open(path).resize((320, 240))
            latest_img = ImageTk.PhotoImage(img)
            tk.Label(dashboard, text="Latest Capture", fg='white', bg='black').pack()
            tk.Label(dashboard, image=latest_img, bg='black').pack()
            dashboard.img_ref = latest_img

        if total > 0:
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.bar(["Success", "Failed"], [success, fail], color=["green", "red"])
            ax.set_title("Login Summary")
            ax.set_ylabel("Attempts")
            canvas = FigureCanvasTkAgg(fig, master=dashboard)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = IntruderCapturer(root)
    root.mainloop()