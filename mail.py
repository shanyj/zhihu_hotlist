import smtplib
from email.mime.text import MIMEText

mail_host = 'smtp.163.com'
# 163用户名
mail_user = 'n8p559n'
# 密码(部分邮箱为授权码)
mail_pass = 'TIXNFNAPGURKSMEB'

# 邮件发送方邮箱地址
sender = 'n8p559n@163.com'
receivers = ['n8p559n@163.com']


def send_email(subject, message):
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers[0]

    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, msg.as_string())
    smtpObj.quit()
