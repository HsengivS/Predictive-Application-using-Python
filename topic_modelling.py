import gensim
from gensim import corpora
from utils import clean_text
from nltk import sent_tokenize
import re


def get_topic_modelling(posted_data, no_of_topics, avg_posted_data, count=1):
    top = {}
    doc_complete = sent_tokenize(posted_data)
    doc_clean = [clean_text(doc).split() for doc in doc_complete]
    dictionary = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    Lda = gensim.models.ldamodel.LdaModel
    if no_of_topics > avg_posted_data:
        no_of_topics = 10
    try:
        ldamodel = Lda(doc_term_matrix, num_topics=no_of_topics,
                       id2word=dictionary, passes=100)
        topics = ldamodel.print_topics(num_topics=no_of_topics,
                                       num_words=5)
    except:
        ldamodel = Lda(doc_term_matrix,
                       num_topics=3,
                       id2word=dictionary,
                       passes=100)
        topics = ldamodel.print_topics(num_topics=3,
                                       num_words=5)
    for i in topics:
        for j in i[1:]:
            word = " ".join(re.findall("[a-zA-Z]+", j))
            out = {str("Topic ")+str(count): word.split()}
            count += 1
            top.update(out)
    return top
