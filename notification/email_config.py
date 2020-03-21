# Email address used to send the notifications
EMAIL_ADDRESS = "better.deal.notifier@gmail.com"
PASSWORD = "betterDeal2020"

# Email address that will receive the notifications
DESTINATION_EMAIL_ADDRESS = "better.deal.notifier@gmail.com"


# List of links to scrape (ideally one should correlate to a car model specified later)
LINKS_TO_SCRAPE = {
    'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/honda-civic/k0c174l1700184', # Honda Civic Ottawa
    'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/mini-cooper/k0c174l1700184' # Mini Cooper Ottawa
}

# List of car models the program will look through in the links given
CAR_MODELS = {
    'Honda Civic',
    'Mini Cooper'
}

# time in seconds between rounds of data collection
TIME_BETWEEN_ROUNDS = 10

# number of rounds to ignore (no email notifications for new cars will be sent for the first ROUNDS_TO_IGNORE rounds)
# this is to avoid overload of notifications at the beginning, when everything is new
ROUNDS_TO_IGNORE = 20