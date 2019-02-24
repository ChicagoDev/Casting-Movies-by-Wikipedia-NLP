import numpy
import math
from nlp.models import Tfidf, TopicModelSVD

@staticmethod
def cosine_distance(u, v):
    """
    Returns the cosine of the angle between vectors v and u. This is equal to
    u.v / |u||v|.
    """
    return numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))




@staticmethod
def get_SVD_model(people):
    docs = [p['stemmed_wiki_doc'] for p in people]
    doc_ids = [p['_id'] for p in people]

    model = Tfidf(docs, doc_ids)
    topic_model = TopicModelSVD(model.model, model.cv_tfidf)

    return (model, topic_model)