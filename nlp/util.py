import numpy
import math
from nlp.models import Tfidf, TopicModelSVD
from sklearn.feature_extraction.text import CountVectorizer
import pickle



def cosine_distance(u, v):
    """
    Returns the cosine of the angle between vectors v and u. This is equal to
    u.v / |u||v|.
    """
    return numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))




def get_SVD_model(people: [dict]):
    docs = [p['clean_doc'] for p in people]
    doc_ids = [p['_id'] for p in people]

    model = Tfidf(docs, doc_ids)
    topic_model = TopicModelSVD(model.model, model.cv_tfidf)

    return (model, topic_model)
