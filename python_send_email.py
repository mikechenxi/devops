#!/usr/bin/python
# -*- coding: utf-8 -*

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from os.path import basename
import smtplib

def send_email(receivers, subject, content, att_paths = None):
    server = "smtp.xxxx.com"
    port = 25
    address = "abc@xxxx.com"
    password = "pwd"

    msg = MIMEMultipart()
    msg["Subject"] = Header(subject, "utf-8")
    msg['From'] = formataddr(["NEW OA", address])
    msg['To'] = receivers
    msg.attach(MIMEText(content, "html", "utf-8"))
    if att_paths is not None and len(att_paths) > 0:
        for att_path in att_paths:
            file = open(att_path, "rb")
            file_name = basename(att_path)
            att = MIMEText(file.read(), "base64", "utf-8")
            att["Content-Type"] = "application/octet-stream"
            att["Content-Disposition"] = "attachment; filename = " + file_name
            file.close()
            msg.attach(att)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(server, port)
        smtp.login(address, password)
        smtp.sendmail(address, receivers.split(","), msg.as_string())
        smtp.quit()
    except smtplib.SMTPException as e:
        print(e)
