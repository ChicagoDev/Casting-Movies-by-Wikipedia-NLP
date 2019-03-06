"""
    This utility file contains code for working with MongoDB
"""

from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId



class CastingPool():

    """

    Easily work with the casting_pool database with this class' helper methods.
    The constructor connects to the localhost Mongo Instance, and needs to be updated. todo

    Instructions: Retrieve people (Wikipedia-Docs) from MongoDB by:

        people = cp.get_casting_pool()
        docs = [p['stemmed_wiki_doc'] for p in people]
        doc_ids = [p['_id'] for p in people]

    """

    db: Collection


    def __init__(self):

        self.client = MongoClient()
        self.client = MongoClient('localhost', 27017)
        #DB named Conan as ode to Conan O'Brien. See: https://www.youtube.com/watch?v=JG74rKtKkKc
        self.db = self.client.conan


    def get_casting_pool(self):
        """
        Retrieve the entire casting_pool Mongo collection
        :return: [dict]
        """

        cast: [dict] = []
        for person in self.db.casting_pool.find():
            cast.append(person)
        return cast


    def get_potential_cast(self, event_id):
        # Retrieve the Mongo DB cast except ones that are within a given event document

        cast: [dict] = []
        excludes = self.db.event.find_one({'_id': event_id})['roles']

        for person in self.db.casting_pool.find({'_id': {'$nin': excludes}}):
            cast.append(person)
        return cast

    def get_roles(self, event_id):

        """

        :param event_id: ObjectID A historic event to cast a movie
        :return: [dict]: A list of People (From MongoDB)
        """

        cast: [dict] = []

        if type(event_id) is str:
            event_id = ObjectId(event_id)

        roles = self.db.events.find_one({'_id': event_id})['roles']

        for person in self.db.event_roles.find({'_id': {'$in': roles}}):
            cast.append(person)
        return cast