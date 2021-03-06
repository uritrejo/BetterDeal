import uuid
import pyrebase
import traceback
import logging


firebaseConfig = {
    'apiKey': "AIzaSyCEE9JHRfzIpuxgtMzFeaZuqw2_DaFkCQY",
    'authDomain': "betterdeals-de427.firebaseapp.com",
    'databaseURL': "https://betterdeals-de427.firebaseio.com",
    'projectId': "betterdeals-de427",
    'storageBucket': "betterdeals-de427.appspot.com",
    'messagingSenderId': "33445910441",
    'appId': "1:33445910441:web:d89aecd987708ff8a916b8",
    'measurementId': "G-J3PE7FMQ4M"
}


# we get the logger
logger = logging.getLogger("BetterDealer")

'''
    Documentation on how to use pyrebase available at:
    https://github.com/thisbejim/Pyrebase
'''


def retrieveSearches():
    print("Retrieve Searches called")
    links = []
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        searches = db.child('Searches').get()
        for search in searches.each():
            links.append(search.val()['Link'])
    except:
        # print("Error retrieving searches, skipping round of collection...")
        logger.exception("Error retrieving searches: ")
        # maybe traceback.print_ex...
        # here you could also save the last of the searches in case it can't retrieve them
        # but at the same time, if this fails, probably its the connection and everything is failing
    # later you could do return links, models
    return links


def retrieveCars():
    links = []
    models = []
    prices = []
    dates = []
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        searches = db.child('Cars').get()
        for search in searches.each():
            print(search.key())
            print(search.val())
            print("Link:", search.val()['Link'])
            print("Model:", search.val()['Model'])
            print("Price:", search.val()['Price'])
            print("Date:", search.val()['Date'])
            links.append(search.val()['Link'])
            models.append(search.val()['Model'])
            prices.append(search.val()['Price'])
            dates.append(search.val()['Date'])
    except:
        logger.exception("Error retrieving cars from the database:")
    return links, models, prices, dates


def addNewSearch(link, model):
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        search = {
            'Model': model,
            'Link': link
        }
        db.child('Searches').push(search)
    except:
        logger.exception("Error adding search.")


def addNewCar(car, link, price, date):
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        new_car = {
            'Model': car,
            'Price': price,
            'Date': date,
            'Link': link
        }
        db.child('Cars').push(new_car)
    except:
        logger.exception("Error adding car.")


def addNewCars(cars, links, prices, dates):
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        dataJSON = {}

        for i in range(len(cars)):
            uid = str(uuid.uuid1())
            dataJSON[uid] = {
                'Model': cars[i],
                'Price': prices[i],
                'Date': dates[i],
                'Link': links[i]
            }
        result = db.child('Cars').set(dataJSON)  # throws the fields directly into the thingy
        print("Cars added: ")
        print(result)
        print("length json = ", str(len(str(dataJSON))), ", length result = ", str(len(str(result))))
    except:
        logger.exception("Error adding cars.")


# This function is only to be used in order to clear test data from the database online
# It deletes teh Cars key and all of its children from the database
def deleteAllCars():
    try:
        fire = pyrebase.initialize_app(firebaseConfig)
        db = fire.database()
        db.child("Cars").remove()
    except:
        print("Error deleting all cars.")
        traceback.print_exc()