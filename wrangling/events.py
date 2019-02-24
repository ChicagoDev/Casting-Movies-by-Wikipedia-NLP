from pymongo import MongoClient, Database




class Events():

    """

    Mongo DB interface for working with cast. Once cast is retrieved, usage as follows:

        docs = [p['stemmed_wiki_doc'] for p in people]
        doc_ids = [p['_id'] for p in people]

    """


    def __init__(self):

        client = MongoClient()
        client = MongoClient('localhost', 27017)
        db = client.conan


    def
        # Retrieves the event's cast in preparation for modeling.

    def
        # Retrieves the event in preparation for modeling