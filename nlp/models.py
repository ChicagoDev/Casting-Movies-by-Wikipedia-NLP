from dataclasses import dataclass
from nltk.corpus import stopwords
from pandas import DataFrame, Index
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


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

    def __init__(self, tfidf_model, vectorizer):

        self.lsa = TruncatedSVD(5)
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