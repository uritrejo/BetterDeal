import smtplib
import notification.email_config
import traceback

def sendEmailNotification(title):
    print(title)
    print(notification.email_config.PASSWORD)

    email_address = notification.email_config.EMAIL_ADDRESS
    password = notification.email_config.PASSWORD

    subject = 'New Ad Posted on a Honda Civic'
    msg = 'Just kidding bro, just testing.'
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email_address, password)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(email_address, email_address, message)
        server.quit()
    except Exception:
        print("Failed to Send Email Notification")
        traceback.print_exc()