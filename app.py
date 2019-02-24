from flask import Flask, request
from wrangling.cast import CastingPool
from bson.json_util import dumps, loads
from sklearn.cluster import KMeans
from nlp.models import Tfidf, TopicModelSVD
from pprint import pprint
from nlp.util import *
from bson import ObjectId

cluster: KMeans = KMeans(10)
tfidf_df_andvec: Tfidf
svd_model: TopicModelSVD

app = Flask(__name__)
casting_pool = CastingPool()
db = casting_pool.db

@app.route('/event', methods=['GET', 'POST'])
def event():
    """
    GET Displays all events in the system.
    POST Primes the KMeans model with given Event. Accepts a single BSON object event.
    """

    if request.method == 'POST':
        event = loads(request.data)
        pprint(event[0]['_id'])
        pprint(event[0]['summary'])

        potential_cast = casting_pool.get_potential_cast(event[0]['_id'])

        global tfidf_df_andvec
        global svd_model
        tfidf_df_andvec, svd_model = get_SVD_model(potential_cast)

        cluster.fit(tfidf_df_andvec.model)


        return 'Cluster Created'

    else:
        events: [dict] = []

        for event in db.event.find():
            events.append(event)

        return dumps(events)



@app.route('/cast', methods=['POST'])
def get_cast():
    """

        POST Retrieves the best match for a given casting. Can be for a single casting or an entire cast.
        """

    req = loads(request.data)

    id: ObjectId = req

    person_to_cast = db.casting_pool.find_one({ '_id': id })
    doc_arr = [person_to_cast['stemmed_wiki_doc']]

    vectorized_person_to_cast = tfidf_df_andvec.cv_tfidf.transform(doc_arr).toarray()

    cluster_predicted = cluster.predict(vectorized_person_to_cast)

    return str(cluster_predicted)

if __name__ == '__main__':
    app.run()
