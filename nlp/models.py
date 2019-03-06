from dataclasses import dataclass
from pandas import DataFrame, Index
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from collections import namedtuple
from bson.objectid import ObjectId
from collections import defaultdict

CastMatch = namedtuple('CastMatch', 'role playedby cosine_dist')

@dataclass
class Tfidf():

    """Returns a TF-IDF Data Frame Model based on a Document Corpus and Document Index

       USAGE:

            client = MongoClient()
            client = MongoClient('localhost', 27017)

            db = client.conan
            casting_pool = db.casting_pool

            people = []

            for person in casting_pool.find():
                people.append(person)

            docs = [p['stemmed_wiki_doc'] for p in people]
            doc_ids = [p['_id'] for p in people]

            tfidf = Tfidf(docs, doc_ids)

"""

    model: DataFrame
    cv_tfidf: TfidfVectorizer

    def __init__(self, corpus, index):

        self.cv_tfidf = TfidfVectorizer(stop_words='english')
        X_tfidf = self.cv_tfidf.fit_transform(corpus).toarray()

        idx = Index(data=index)

        self.model = DataFrame(X_tfidf, columns=self.cv_tfidf.get_feature_names(), index=idx)



class TopicModelSVD():

    """Create SVD Topic Model for a given TFIDF DataFrame and Vectorizor. Displays Topics

        USAGE:

        model = Tfidf(docs, doc_ids)

        topic_model = TopicModelSVD(model.model, model.cv_tfidf)

        topic_model.display_topics(5)

    """

    lsa: TruncatedSVD
    cv_tfidf: TfidfVectorizer

    def __init__(self, tfidf_model, vectorizer, n_topics=50):

        self.lsa = TruncatedSVD(n_topics)
        self.lsa.fit_transform(tfidf_model)
        self.cv_tfidf = vectorizer


    def display_topics(self, no_top_words, topic_names=None):
        for ix, topic in enumerate(self.lsa.components_):
            if not topic_names or not topic_names[ix]:
                print("\nTopic ", ix)
            else:
                print("\nTopic: '", topic_names[ix], "'")
            print(", ".join([self.cv_tfidf.get_feature_names()[i]
                             for i in topic.argsort()[:-no_top_words - 1:-1]]))





def get_cluster_as_dict(means):
    """
        Data Conversion. Converts a Cluster to a Dict[list].
        Keys-> Clusternames, Values -> Cluster Members
    """
    clust_raw = means.predict(doc_topix_matx)
    clusters = defaultdict(list)
    for clust in zip(clust_raw, doc_topix_matx.index):
        clusters[clust[0]].append(clust[1])
    return clusters




def get_roles(event_id, db):
    """
        Cast retrieval from DB. Returns a List[dict] of cast, given an event from the database.
    """

    cast: [dict] = []

    if type(event_id) is str:
        event_id = ObjectId(event_id)

    roles = db.events.find_one({'_id': event_id})['roles']

    for person in db.event_roles.find({'_id': { '$in': roles}}):
        cast.append(person)
    return cast


def best_match(got_roles_list, clust_dict, vectorizer, topic_model, cluster_model):
    """
        Searches a cluster for the most similar actor.

    """
    matches = []

    for person in got_roles_list:

        best_match = None
        best_fit = -np.inf

        words = vectorizer.transform([person['clean_doc']]).toarray()
        words_reduced = topic_model.transform(words)
        persons_cluster = cluster_model.predict(words_reduced)

        for cast in clust_dict[persons_cluster[0]]:

            cluster_person = [model_a.model.loc[cast]]
            topic_model_person = topic_model.transform(cluster_person)
            cos_dist = cosine_distance(words_reduced[0], topic_model_person[0])

            if cos_dist > best_fit:
                best_fit = cos_dist
                best_match = cast

        matches.append(CastMatch(role=person['name'], playedby=best_match, cosine_dist=best_fit))

    return matches





def get_real_actor(cast_match):
    """
        Creates a human-readable named-tuple from a match object with a Mongo _id
    """

    role = cast_match.role
    person = cast.find_one({'_id': cast_match.playedby})
    dist = cast_match.cosine_dist
    return CastMatch(role, person['name'], dist)