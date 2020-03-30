# Email address used to send the notifications
EMAIL_ADDRESS = "better.deal.notifier@gmail.com"
PASSWORD = "betterDeal2020"

# Email address that will receive the notifications
DESTINATION_EMAIL_ADDRESS = "better.deal.notifier@gmail.com"


# List of links to scrape (ideally one should correlate to a car model specified later)
LINKS_TO_SCRAPE = {
    # 'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/honda-civic/k0c174l1700184', # Honda Civic Ottawa
    # 'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/mini-cooper/k0c174l1700184', # Mini Cooper Ottawa
    'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/gmc-yukon/2016__/k0c174l1700184a68', # GMC Yukon > 2016
    'https://www.kijiji.ca/b-cars-trucks/ottawa-gatineau-area/dodge-ram-rebel/2019__/k0c174l1700184a68' # Dodge RAM Rebel 2019-2020
}

# List of car models the program will look through in the links given
CAR_MODELS = {
    'Honda Civic',
    'Mini Cooper',
    'Dodge RAM Rebel 2019',
    'Dodge RAM Rebel 2020',
    'GMC Yukon 2016',
    'GMC Yukon 2017',
    'GMC Yukon 2018',
    'GMC Yukon 2019',
    'GMC Yukon 2020',
}

# time in seconds between rounds of data collection
TIME_BETWEEN_ROUNDS = 240

# number of rounds to ignore (no email notifications for new cars will be sent for the first ROUNDS_TO_IGNORE rounds)
# this is to avoid overload of notifications at the beginning, when everything is new
ROUNDS_TO_IGNORE = 10
