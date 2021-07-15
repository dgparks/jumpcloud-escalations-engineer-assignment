import pymongo
from datetime import datetime

# initialize mongo client
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['brewery']

def main():
    now = str(datetime.now()).replace(' ', '_').replace(':', "-")
    with open ('out/brewery-{}.txt'.format(now), 'w') as f:

        #
        # ALL PATRONS
        #
        f.write("\nname and email of every patron:\n")
        all_patrons = db.patrons.find({}, {'_id': 0, 'full_name': 1, 'email': 1})
        for patron in all_patrons:
            f.write(str(patron) + '\n')
        
        #
        # IPA LOVERS
        #
        f.write("\nname and email of every patron whose favorite beer is IPA:\n")
        for lover in get_ipa_lovers():
            f.write(str(lover) + '\n')

        #
        # TAPROOM VISITS
        #
        f.write("\nper taproom count of patrons that last visited between 1/1/2021 - 4/1/2021:\n")
        for taproom in get_taproom_visits(datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 4, 1, 0, 0, 0)):
            f.write(str(taproom) + '\n')

        #
        # BEER STATS
        #
        f.write("\nlist of each beer with its type and its frequency as a favorite:\n")
        for beer in get_beer_stats():
            f.write(str(beer) + '\n')

def get_ipa_lovers():
    return list(db.patrons.aggregate([
        {
            '$lookup': {
                'from': 'beers',
                'localField': 'favorite_beer',
                'foreignField': '_id',
                'as': 'favorite_beer_details'
            }
        },
        { '$unwind': '$favorite_beer_details' },
        {
            '$project': {
                '_id': 0,
                'first_name': 1,
                'last_name': 1,
                'email': 1,
                'type': '$favorite_beer_details.type'
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
                'as': 'favorite_beer_details'
            }
        },
        { '$unwind': '$favorite_beer_details' },
        { '$group' : { '_id' : '$favorite_beer_details.name', 'count' : {'$sum' : 1}} },
        {
            '$project': {
                '_id': 0,
                'name': "$_id",
                'type': "$favorite_beer_details.type",
                'count': "$count"
            }
        },
    ]))

if __name__ == "__main__":
    main()