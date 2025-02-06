import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os  # 用于读取 GitHub Secrets 环境变量

# 网站和邮箱配置
URL = os.getenv("MONITOR_URL")  # 需要监控的网站
EMAIL_FROM = os.getenv("EMAIL_FROM")          # 发件邮箱（163邮箱）
EMAIL_TO = os.getenv("EMAIL_TO")              # 收件人邮箱
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # 163邮箱授权码（不是登录密码）

def check_website():
    try:
        response = requests.get(URL, timeout=10)
        if response.status_code == 200:
            print(f"✅ {URL} 正常运行。")
        else:
            print(f"⚠️ {URL} 状态异常：{response.status_code}")
            send_email_alert(f"网站状态异常：{response.status_code}")
    except requests.RequestException:
        print(f"❌ 无法访问 {URL}")
        send_email_alert("网站无法访问！")

def send_email_alert(message):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"🚨 网站监控警报：{URL}"

    msg.attach(MIMEText(message, "plain"))

    # 163 SMTP服务器配置
    smtp_server = "smtp.163.com"
    smtp_port = 465  # SSL端口

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
            print("📧 报警邮件已发送。")
    except Exception as e:
        print(f"❌ 发送邮件失败：{e}")

if __name__ == "__main__":
    check_website()
