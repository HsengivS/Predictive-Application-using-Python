from nltk.corpus import stopwords
import string
from nltk.stem.wordnet import WordNetLemmatizer
from pymongo import MongoClient
from constants import CONNECTION_STRING

client = MongoClient(CONNECTION_STRING)
db = client.PROJECTS
col = db['nlp_apps']

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean_text(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    less_than_3 = " ".join([i for i in normalized.lower().split() if len(i) > 3])
    return less_than_3


def counttokens(username):
    credit = col.find_one({"Username": username})['tokens']
    # credits = credit.get('tokens')
    print(credit)
    return credit









#
