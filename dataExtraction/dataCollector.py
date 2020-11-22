import csv
from notification.notification_manager import *
import config
import database.database as db
from datetime import date

# When the local list reaches this size, it will write its values into a csv file and clear the local list
MAX_ADS_IN_ARRAYS = 1500  # to be fully tested, 1200 sounds okay for now, think about it more logically
# when we get to MAX_ADS_IN_ARRAYS, only the last WINDOW_TO_STORE added elems will be kept in the arrays
WINDOW_TO_STORE = 10000
# the price will be set to this whenever the price for a given ad is smt like: "PLEASE CONTACT"
NON_NUMERIC_PRICE = -1

KIJIJI_BASE = 'https://www.kijiji.ca'

# This is where the car data is going to be stored
# We could potentially use a list of lists, each for a given car model
cars = []
prices = []  # now stored as strings, but we'll have to move into storing them as floats
links = []  # strings containing the link to the posting (may be better to use this for comparisons)
dates = []  # the dates when the the given car was posted

searchRounds = {}  # will contain the round counter for every search that is added on the database

# can be removed when cleaning csv functionalities
# will be used to only add the unadded ads on the csv
ad_index = -1


# this function processes the data given by the spider and stores it into the respective arrays
def processNewData(currentRequestURL, strippedExtractedCars, strippedExtractedPrices, strippedExtractedLinks):
    global searchRounds

    # now we check onto our global list if the given car extracted had already been processed
    # if it hadn't, then we send a notification
    if (len(strippedExtractedCars) == len(strippedExtractedPrices) and
            len(strippedExtractedCars) == len(strippedExtractedLinks)):  # now we also compare the length of the links

        # we get the date
        today_date = date.today()
        # dd/mm/YY
        today = today_date.strftime("%Y/%m/%d")

        # if it ever becomes a requirement, we could get the exact time this way:
        # now = datetime.now()
        # current_time = now.strftime("%H:%M:%S")

        # we check if it's new, we print the new ones
        # if new, we add both the car and the price
        # we could also add a counter to avoid notifying within the first rounds

        # this list will contain the lists of cars, prices adn links of the new cars to notify
        carsToNotify = []
        pricesToNotify = []
        linksToNotify = []

        for i in range(0, len(strippedExtractedCars)):

            newCar = strippedExtractedCars[i]
            carPrice = strippedExtractedPrices[i]
            carLink = strippedExtractedLinks[i]

            # if newCar not in cars:  # if it's a new posting, we notify and we add it (we might wanna compare
            # the links now instead of the titles)
            if carLink not in links:  # if it's a new posting, we notify and we add it

                print("New Car:\n", newCar, "\n", carPrice)

                # the links from kijijiauto come complete (https://kijijauto...)
                # but fot he kijiji ones, we must add the base of the link (they always start with /)
                if carLink[0] == '/':
                    carLink = KIJIJI_BASE + carLink

                # now we strip the price from the dollar sign and the commas to try and parse it as a 'double'

                try:
                    formattedCarPrice = carPrice.strip('$').replace(',', '')
                    numericCarPrice = float(formattedCarPrice)
                except:
                    # if we fail to convert it to a float, then we add a -1 (maybe a 0 would be good) to show the error
                    print("Price: " + carPrice + " couldn't be parsed as a double.")
                    numericCarPrice = -1
                    traceback.print_exc()

                #  we add them into the global list
                cars.append(newCar)
                prices.append(numericCarPrice)
                links.append(carLink)
                dates.append(today)

                # we add them to the list of cars to modify for this round
                carsToNotify.append(newCar)
                pricesToNotify.append(carPrice)
                linksToNotify.append(carLink)

                # we add the car to the database
                db.addNewCar(newCar, carLink, numericCarPrice, today)

                # using the following lines, each ad would be notified on a separate email, instead of a group
                # if searchRounds[currentRequestURL] > config.ROUNDS_TO_IGNORE:
                #     sendEmailNotification(newCar, carPrice, carLink)  # for email, the non numeric price looks better

        # we send the email with the cars to notify
        if searchRounds[currentRequestURL] > config.ROUNDS_TO_IGNORE:
            sendEmailNotificationM(carsToNotify, pricesToNotify, linksToNotify)

        # we are only keeping in memory the most recent ads, once it crosses the maximum
        # threshold, we clear the last few
        if len(cars) > MAX_ADS_IN_ARRAYS:
            clearPartialMemory()

    else:  # we have a different number of cars and prices, we can't compare
        print("\nAttention: Data in this round of collection was corrupted. " +
              "Posts won't update until next round of collection.\n")

    searchRounds[currentRequestURL] += 1


# helper method
# erases all of the car and prices arrays except for the last WINDOW_TO_STORE elems
#   this is done in order to save memory, but still have a relative window to tell
#   if the newest elems are repeated or if they should be notified
# Remark: it doesn't erase the csv file
def clearPartialMemory():
    global cars, prices, links, dates, ad_index

    # about 10MB of data (10000) cars will be kept stored
    oldSize = len(cars)

    # we keep only the last values added into the lists
    cars = cars[len(cars) - WINDOW_TO_STORE:len(cars)]
    prices = prices[len(prices) - WINDOW_TO_STORE:len(prices)]
    links = links[len(links) - WINDOW_TO_STORE:len(links)]
    dates = dates[len(dates) - WINDOW_TO_STORE:len(dates)]

    # we also update the date index so that it's still aligned (for the CSV file)
    ad_index = WINDOW_TO_STORE

    print("Memory cleared, from old size: ", oldSize, " new sizes are: ", len(cars), len(prices), len(links), len(dates))


# DEPRECATED, BUT WILL BE REUSED WHITHIN THE UI, SO KEEP THE CODE
# WONT BE USED FOR NOW, REPLACED BY FIREBASE
# writes the collected cars into a csv file (excluding the links, might change later)
def exportDataToCSV():
    global ad_index

    appendToCSV = 'a'
    if ad_index == -1:  # this would be true if it's the first file ot be written
        appendToCSV = 'w'

    try:
        with open('data.csv', appendToCSV) as file:
            # with open('data.csv', appendToCSV, newline='') as file: # This version wouldnt work on linux
            writer = csv.writer(file)
            # we initialize the titles if it is the first to be written
            if ad_index == -1:
                writer.writerow(["Car Model".encode('utf8'), "Price".encode('utf8')])
                ad_index += 1

            # we write each of the new cars in a row at the end of the file
            for i in range(ad_index, len(cars)):
                writer.writerow([cars[i].encode('utf8'), prices[i].encode('utf8')])
                ad_index += 1

            print("Data was succesfully written")

            if len(cars) > MAX_ADS_IN_ARRAYS:
                clearPartialMemory()

    except Exception:
        traceback.print_exc()


'''
    Will create an entry into the dictionary of counts, if it's already there, 
    it will leave it untouched
'''
def updateSearchesCount(links):
    global searchRounds
    for link in links:
        if link not in searchRounds:
            searchRounds[link] = 1
