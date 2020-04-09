import smtplib
# import notification.email_config
import config
import traceback

def sendEmailNotification(ad_title, price, link):

    email_address = config.EMAIL_ADDRESS
    password = config.PASSWORD
    destination_address = config.DESTINATION_EMAIL_ADDRESS

    # The exact contents of the email are subject to change
    subject = ad_title
    msg = 'Price: ' + price + '\n' + 'https://www.kijiji.ca' + link

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