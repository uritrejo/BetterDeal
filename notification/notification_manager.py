import smtplib
import notification.email_config
import traceback

def sendEmailNotification(ad_title, price):

    email_address = notification.email_config.EMAIL_ADDRESS
    password = notification.email_config.PASSWORD
    destination_address = notification.email_config.DESTINATION_EMAIL_ADDRESS

    # The exact contents of the email are subject to change
    subject = ad_title
    msg = 'Price: ' + price

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(email_address, password)
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail(email_address, destination_address, message)
        server.quit()
        print("Notification email sent succesfully!")
    except Exception:
        print("Failed to Send Email Notification")
        traceback.print_exc()