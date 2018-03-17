# =*= coding: utf=8 =*
import smtplib
from email.mime.text import MIMEText

sender = 'nobug@sequee.com'
smtpserver = 'smtp.exmail.qq.com'
username = 'nobug@sequee.com'
password = 'jUEdUImEIbUG2019'


def send_alert_email_to(to_addrs, ccs, content, subject):
    '''to_addrs: A list of addresses to send this mail to
    ccs :A list of addresses to copy this mail to
    content: email content'''
    msg = MIMEText(content, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ",".join(to_addrs)
    msg['Cc'] = ",".join(ccs)
    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, to_addrs + ccs, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    to_address = ["517465107@qq.com"]
    ccs = ["xiahaijiao@pku.edu.cn"]
    send_alert_email_to(to_address, ccs, "hello world")
    # print "done!"
