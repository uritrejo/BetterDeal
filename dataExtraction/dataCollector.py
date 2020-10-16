import csv
from notification.notification_manager import *
import config
import database.database as db

# This is where the car data is going to be stored
# We could potentially use a list of lists, each for a given car model
cars = []
prices = [] # now stored as strings, but we'll have to move into storing them as floats
links = [] # strings containing the link to the posting (may be better to use this for comparisons)
removedPrices = []
round = 1

# will be used to only add the unadded ads
ad_index = -1

# When the local list reaches this size, it will write its values into a csv file and clear the local list
MAX_ADS_IN_ARRAYS = 1200  # to be fully tested, 1200 sounds okay for now, think about it more logically
# when we get to MAX_ADS_IN_ARRAYS, only the last WINDOW_TO_STORE added elems will be kept in the arrays
WINDOW_TO_STORE = 200
# the price will be set to this whenever the price for a given ad is smt like: "PLEASE CONTACT"
NON_NUMERIC_PRICE = -1


# this function processes the data given by the spider and stores it into the respective arrays
def processNewData(strippedExtractedCars, strippedExtractedPrices, strippedExtractedLinks):
    global round

    # now we check onto our global list if the given car extracted had already been processed
    # if it hadn't, then we send a notification
    if (len(strippedExtractedCars) == len(strippedExtractedPrices) and
            len(strippedExtractedCars) == len(strippedExtractedLinks)):  # now we also compare the length of the links

        # initialization for the arrays that will be passed to the database
        newCars = []
        newPrices = []
        newLinks = []

        # we check if it's new, we print the new ones
        # if new, we add both the car and the price
        # we could also add a counter to avoid notifying within the first rounds

        for i in range(0, len(strippedExtractedCars)):

            newCar = strippedExtractedCars[i]
            carPrice = strippedExtractedPrices[i]
            carLink = strippedExtractedLinks[i]

            # if newCar not in cars:  # if it's a new posting, we notify and we add it (we might wanna compare the links now instead of the titles)
            if carLink not in links:  # if it's a new posting, we notify and we add it

                print("New Car:\n", newCar, "\n", carPrice, "\n", carLink)
                # we add them into the global list
                cars.append(newCar)
                prices.append(carPrice)
                links.append(carLink)

                # we add them into the database lists
                newCars.append(newCar)
                newPrices.append(carPrice)
                newLinks.append(carLink)

                if round > config.ROUNDS_TO_IGNORE:
                    sendEmailNotification(newCar, carPrice, carLink)

        # we are only keeping in memory the most recent ads, once it crosses the maximum
        # threshold, we clear the last few
        if len(cars) > MAX_ADS_IN_ARRAYS:
            clearPartialMemory()

        if len(newCars) > 0:
            db.addNewCars(newCars, newLinks, newPrices)


    else:  # we have a different number of cars and prices, we can't compare
        print("\nTragedie:\nStripped Cars: ", len(strippedExtractedCars), "\nStripped Prices: ",
              len(strippedExtractedPrices), "\nStripped Links: ", len(strippedExtractedLinks))

    round += 1


# helper method
# erases all of the car and prices arrays except for the last WINDOW_TO_STORE elems
#   this is done in order to save memory, but still have a relative window to tell
#   if the newest elems are repeated or if they should be notified
# Remark: it doesn't erase the csv file
def clearPartialMemory():

    global cars, prices, links, ad_index

    oldSize = len(cars)

    # we keep only the last values added into the lists
    cars = cars[len(cars)-WINDOW_TO_STORE:len(cars)]
    prices = prices[len(prices)-WINDOW_TO_STORE:len(prices)]
    links = links[len(links)-WINDOW_TO_STORE:len(links)]

    # we also update the date index so that it's still aligned
    ad_index = WINDOW_TO_STORE

    print("Memory cleared, from old size: ", oldSize, " new sizes are: ", len(cars), len(prices), len(links))


# WONT BE USED FOR NOW, REPLACED BY FIREBASE
# writes the collected cars into a csv file (excluding the links, might change later)
def exportDataToCSV():

    global ad_index

    appendToCSV = 'a'
    if(ad_index == -1): # this would be true if it's the first file ot be written
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