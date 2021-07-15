import pymongo, json, logging
from datetime import datetime

# set filenames and configure logging
now = str(datetime.now()).replace(' ', '_').replace(':', "-")
log_file = 'log/brewery-' + now + '.log'
out_file = 'out/brewery-' + now + '.json'
logging.basicConfig(filename=log_file, level=logging.INFO)

# initialize mongo client
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['brewery']

# query data and write results to a json file in /out
def main():
    brewery = [
        { 'all_patrons': get_all_patrons() },
        { 'ipa_lovers': get_ipa_lovers() },
        { 'taproom_visits': get_taproom_visits(datetime(2021, 1, 1, 0, 0, 0), datetime(2021, 4, 1, 0, 0, 0)) },
        { 'beer_stats': get_beer_stats() }
    ]
    try:
        with open (out_file, 'w') as f:
            json.dump(brewery, f)
        logging.info('Successfully wrote \'brewery\' to \'{}\''.format(out_file))
    except Exception as e:
        logging.error(e)

def get_all_patrons():
    """ return a list containing the name and email of every patron """
    try:
        response = list(db.patrons.find({}, {'_id': 0, 'first_name': 1, 'last_name': 1, 'email': 1}))
        logging.info('Successfully retrieved {} patrons.'.format(len(response)))
        return response
    except Exception as e:
        logging.error(e)
        return []

def get_ipa_lovers():
    """ return a list containing the name and email of every patron whose favorite beer is IPA """
    try:
        response = list(db.patrons.aggregate([
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
        logging.info('Successfully retrieved {} ipa_lovers.'.format(len(response)))
        return response
    except Exception as e:
        logging.error(e)
        return []

def get_taproom_visits(start, end):
    """
    per taproom count of patrons that last visited within a range of dates

    :param start: ISODate representing the start of the desired date range
    :param end: ISODate representing the end of the desired date range
    """
    try:
        response = list(db.patrons.aggregate([
            { 
                '$match': { 
                    'last_checkin': {'$gte': start, '$lt': end}
                }
            },
            { '$group' : { '_id' : '$location', 'count' : {'$sum' : 1}} }
        ]))
        logging.info('Successfully retrieved taproom_visits.')
        return response
    except Exception as e:
        logging.error(e)
        return []

def get_beer_stats():
    """ return a list of each beer with its type and its frequency as a favorite """
    try:
        response = list(db.patrons.aggregate([
            {
                '$lookup': {
                    'from': 'beers',
                    'localField': 'favorite_beer',
                    'foreignField': '_id',
                    'as': 'favorite_beer_details'
                }
            },
            { '$unwind': '$favorite_beer_details' },
            { '$group' : { '_id' : '$favorite_beer_details.name', 'type': {'$addToSet': '$favorite_beer_details.type'}, 'count' : {'$sum' : 1}} },
            {
                '$project': {
                    '_id': 0,
                    'name': "$_id",
                    'type': { 
                        '$reduce': { 
                            'input': "$type", 'initialValue': "",
                            'in': { '$concat' : ["$$value", "$$this"] } 
                        }
                    },
                    'count': "$count"
                }
            },
        ]))
        logging.info('Successfully retrieved beer_stats.')
        return response
    except Exception as e:
        logging.error(e)
        return []

if __name__ == "__main__":
    main()