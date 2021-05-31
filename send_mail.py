import smtplib


def send_email(host, subject, to_addr, from_addr, body_text):
    """
    Send an email
    """

    BODY = "\r\n".join((
        "From: %s" % from_addr,
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "",
        body_text
    )).encode('utf-8')

    server = smtplib.SMTP(host, 587)
    server.starttls()
    server.login(from_addr, 'mgnbqnrtmkbzqjxg')
    server.sendmail(from_addr, [to_addr], BODY)
    server.quit()


if __name__ == "__main__":
    host = "smtp.gmail.com"
    subject = "Test email from Python"
    to_addr = "radikkhabibulin@mail.ru"
    from_addr = "radikmkhabibulin@gmail.com"
    body_text = "Python rules them all!"
    send_email(host, subject, to_addr, from_addr, body_text)
