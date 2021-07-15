import pymongo
from datetime import datetime

# initialize mongo client
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['brewery']

def main():
    print("\nname and email of every patron:")
    all_patrons = db.patrons.find({}, {'_id': 0, 'full_name': 1, 'email': 1})
    print(all_patrons)
    
    print("\nname and email of every patron whose favorite beer is IPA")
    for lover in get_ipa_lovers():
        print(lover)

    print("\nper taproom count of patrons that last visited between 1/1/2021 - 4/1/2021")
    for taproom in get_taproom_visits(datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 4, 1, 0, 0, 0)):
        print(taproom)

    print("\nlist of each beer with its type and its frequency as a favorite")
    for beer in get_beer_stats():
        print(beer)

def get_ipa_lovers():
    return list(db.patrons.aggregate([
        {
            '$lookup': {
                'from': 'beers',
                'localField': 'favorite_beer',
                'foreignField': '_id',
                'as': 'beer'
            }
        },
        { '$unwind': '$beer' },
        {
            '$project': {
                '_id': 0,
                'first_name': 1,
                'last_name': 1,
                'email': 1,
                'type': '$beer.type'
            }
        },
        { '$match': {'type': "IPA"}}
    ]))

def get_taproom_visits(start, end):
    """
    :param start: ISODate representing the start of the desired date range
    :param end: ISODate representing the end of the desired date range
    """
    return list(db.patrons.aggregate([
        { 
            '$match': { 
                'last_checkin': {'$gte': start, '$lt': end}
            }
        },
        { '$group' : { '_id' : '$location', 'count' : {'$sum' : 1}} }
    ]))


def get_beer_stats():
    return list(db.patrons.aggregate([
        {
            '$lookup': {
                'from': 'beers',
                'localField': 'favorite_beer',
                'foreignField': '_id',
                'as': 'beer'
            }
        },
        { '$unwind': '$beer' },
        { '$group' : { '_id' : '$beer.name', 'count' : {'$sum' : 1}} },
        {
            '$project': {
                '_id': 0,
                'name': "$_id",
                'type': "$beer.type",
                'count': "$count"
            }
        },
    ]))

if __name__ == "__main__":
    main()