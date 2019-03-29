import spacy
import re
import tldextract
from urlextract import URLExtract

from constants import PHONE_NUMBER_PATTERN1, PHONE_NUMBER_PATTERN2, EMAIL_PATTERN, URL_REGEX
from utils import clean_text


nlp_spacy = spacy.load('models/en_core_web_sm')
nlp_resume = spacy.load('models/resume_model')


# EXTRACT EMAIL
def get_mail(text):
    mailId = re.findall(EMAIL_PATTERN, text)
    if len(mailId) < 1:
        return mailId
    else:
        return mailId[0]


def get_mail_list(text):
    mailId = re.findall(EMAIL_PATTERN, text)
    return mailId[0]


# EXTRACT PHONE NUMBER
def get_phone_number(text):
    try1 = re.findall(PHONE_NUMBER_PATTERN1, text)
    try2 = []
    if try1 == []:
        try2.append(re.findall(PHONE_NUMBER_PATTERN2, text))
        return try2[0]
    else:
        return try1[0]


# EXTRACT URL
def get_url(text):
    a = []
    urls = re.findall(URL_REGEX, text)
    Urls = list(set(urls))
    Urls = list(set([i for i in Urls if len(i) > 9]))
    if Urls == []:
        extractor = URLExtract()
        anotherWayUrls = extractor.find_urls(text)
        anotherWayUrls = list(set([i for i in anotherWayUrls if len(i) > 9]))
        if anotherWayUrls == []:
            a.append('')
            return a
        return anotherWayUrls
    else:
        return Urls


# EXTRACT URL
def get_url_with_domain(text, count):
    url_arr = []
    url_list = get_url(text)
    for url in url_list:
        parsed_url = tldextract.extract(url)
        domain_name = parsed_url.domain
        try:
            url_dic = {str(count)+" URL "+(domain_name).upper(): url}
            count += 1
            url_arr.append(url_dic)
        except:
            pass
    return url_arr


def get_spacy_ner(posted_data, nlp_spacy):
    result_dict = {}
    doc = nlp_spacy((posted_data.lower()))
    print(result_dict)
    count = 1
    for entity in doc.ents:
        out = {str(count)+str(" ")+(entity.label_).upper(): entity.text}
        count += 1
        result_dict.update(out)
    return result_dict


def get_resume_ner(posted_data, nlp_resume):
    result_dict = {"1 EMAIL": get_mail_list(posted_data),
                   "2 CONTACT NUMBER": get_phone_number(clean_text(posted_data))}
    doc = nlp_resume(posted_data.lower())
    count = 3
    for entity in doc.ents:
        out = {str(count)+str(" ")+(entity.label_).upper(): entity.text}
        count += 1
        result_dict.update(out)
    for url in get_url_with_domain(posted_data, count):
        result_dict.update(url)
    return result_dict
