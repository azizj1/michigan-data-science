import pickle
import gensim
from gensim.models.ldamodel import LdaModel
from gensim.matutils import Sparse2Corpus
from sklearn.feature_extraction.text import CountVectorizer


def lda_model():

    # Load the list of documents
    with open('newsgroups', 'rb') as f:
        newsgroup_data = pickle.load(f)

    # Use CountVectorizor to find three letter tokens, remove stop_words, 
    # remove tokens that don't appear in at least 20 documents,
    # remove tokens that appear in more than 20% of the documents
    vect = CountVectorizer(min_df=20, max_df=0.2, stop_words='english', 
                        token_pattern='(?u)\\b\\w\\w\\w+\\b')
    # Fit and transform
    X = vect.fit_transform(newsgroup_data)

    # Convert sparse matrix to gensim corpus.
    corpus = Sparse2Corpus(X, documents_columns=False)

    # Mapping from word IDs to words (To be used in LdaModel's id2word parameter)
    id_map = dict((v, k) for k, v in vect.vocabulary_.items())

    # Use the gensim.models.ldamodel.LdaModel constructor to estimate
    # LDA model parameters on the corpus, and save to the variable `ldamodel`

    return vect, LdaModel(corpus, num_topics=10, id2word=id_map, passes=25, random_state=34)

def lda_topics(model: LdaModel):
    return model.show_topics()

def topic_distribution(vect: CountVectorizer, model: LdaModel):
    new_doc = ["\n\nIt's my understanding that the freezing will start to occur because \
    of the\ngrowing distance of Pluto and Charon from the Sun, due to it's\nelliptical orbit. \
    It is not due to shadowing effects. \n\n\nPluto can shadow Charon, and vice-versa.\n\nGeorge \
    Krumins\n-- "]
    bow = Sparse2Corpus(vect.transform(new_doc), documents_columns=False)
    return next(iter(model[bow]), None)
