from pymongo import MongoClient, Database




class CastingPool():

    """

    Mongo DB interface for working with cast. Once cast is retrieved, usage as follows:

        docs = [p['stemmed_wiki_doc'] for p in people]
        doc_ids = [p['_id'] for p in people]

    """

    db: Database
    cast: []

    def __init__(self):

        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.conan


    def get_cast(self):

        for person in self.db.find():
            self.cast.append(person)

    def get_potential_cast(self, event):
        # Retrieve the Mongo DB cast except ones that are within a given event document
        pass