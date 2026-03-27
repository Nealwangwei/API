# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# =====================================
# 1️⃣ 作家身份生成内容
# =====================================
def write_story():
    """
    模拟作家身份写一篇短文
    """
    story = """
    亲爱的朋友，

    今天我坐在窗前，看着雨丝轻轻落下，心中涌起了无尽的思绪。
    每一次文字的敲击，仿佛都是心灵的回声。
    希望你读到这些文字时，也能感受到这份宁静与温暖。

    期待你的回信。

    你的朋友，
    作家
    """
    return story

# =====================================
# 2️⃣ 邮件配置
# =====================================
sender_email = "osun12347@gmail.com"
receiver_email = "osun12347@gmail.com"
password = "你的邮箱授权码"  # Gmail SMTP 需要使用 App Password

subject = "一封作家写给朋友的信"

# =====================================
# 3️⃣ 构建邮件
# =====================================
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

# 添加正文
body = write_story()
message.attach(MIMEText(body, "plain"))

# =====================================
# 4️⃣ 发送邮件（Gmail SMTP）
# =====================================
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    server.quit()
    print("邮件发送成功！")
except Exception as e:
    print("邮件发送失败:", e)