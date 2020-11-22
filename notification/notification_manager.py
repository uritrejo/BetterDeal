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
    msg = 'Price: ' + price + '\n' + link

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


# sends an email notification with all the new cars of the round
def sendEmailNotificationM(ad_titles, prices, links):

    email_address = config.EMAIL_ADDRESS
    password = config.PASSWORD
    destination_address = config.DESTINATION_EMAIL_ADDRESS

    # The exact contents of the email are subject to change
    subject = "New Cars Posted!"
    msg = ""
    for i in range(len(ad_titles)):

        # we are gonna eliminate characters that ascii cant parse
        # smtp has problems with these characters and produces errors
        # there is a risk that if the links contain one of these characters, we'll make the link useless
        # however, a broken link is better than no email at all
        ad_title = ad_titles[i].encode('ascii', 'ignore').decode('ascii')
        price = prices[i].encode('ascii', 'ignore').decode('ascii')
        link = links[i].encode('ascii', 'ignore').decode('ascii')

        msg = msg + str(i+1) + ": " + ad_title + "\nPrice: " + price + "\n" + link + "\n\n"

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
