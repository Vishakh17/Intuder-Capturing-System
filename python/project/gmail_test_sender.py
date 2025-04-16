import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 🔐 Replace these with your Gmail and App Password
sender_email = "vishakhshetty310@gmail.com"
sender_password = "bltf anok arvk hxih"

# 📩 Receiver (you can use your same Gmail for test)
receiver_email = "vishakhshetty5@gmail.com"

# ✉️ Email content
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = "✅ Test Email from Python"

body = "This is a test email sent using Python. If you receive this, SMTP is working!"
msg.attach(MIMEText(body, 'plain'))

try:
    print("📡 Connecting to Gmail SMTP server...")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    print("🔐 Logging in...")
    server.login(sender_email, sender_password)
    print("📤 Sending message...")
    server.send_message(msg)
    server.quit()
    print("✅ Test email sent successfully!")
except Exception as e:
    print("❌ Failed to send email:", e)
