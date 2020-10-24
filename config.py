# Email address used to send the notifications
EMAIL_ADDRESS = "better.deal.notifier@gmail.com"
PASSWORD = "betterDeal2020"

# Email address that will receive the notifications, potentially make it a list?
DESTINATION_EMAIL_ADDRESS = "better.deal.notifier@gmail.com"


# time in seconds between rounds of data collection
TIME_BETWEEN_ROUNDS = 30
# TIME_BETWEEN_ROUNDS = 10

# number of rounds to ignore (no email notifications for new cars will be sent for the first ROUNDS_TO_IGNORE rounds)
# this is to avoid overload of notifications at the beginning, when everything is new
ROUNDS_TO_IGNORE = 10
