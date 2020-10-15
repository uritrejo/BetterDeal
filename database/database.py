from firebase import firebase

def retrieveCars():
    print("Retrieving cars from database...\n")
    db = firebase.FirebaseApplication("https://betterdeals-de427.firebaseio.com/", None);
    result = db.get('/betterdeals-de427/Car', '')
    print(result)

# retrieveAllCars

# insertManyCars
    # potentially a data formating into json for this one
    # make sure where the changes have to be made to do this.
    # probably keep the circular list anyways, you cant always retrieve your shit from firebase
    # you can keep a local list of the new changes and then pass the list as a whole to a method
    # bref, the add cars has to be for adding a list of cars, not only one or two

# check if you can decide the key (seria el kijiji announcement)

# retrieveLinks
# add links

def retrieveLinks():
    print("Retrieving cars from database...\n")
    db = firebase.FirebaseApplication("https://betterdeals-de427.firebaseio.com/", None);
    result = db.get('/betterdeals-de427/Link', '')
    print(result)




# todo:
    # erase the shit
    # design interface