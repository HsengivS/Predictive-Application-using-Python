import spacy
nlp_spacy = spacy.load('models/en_core_web_sm')
nlp_resume = spacy.load('models/resume_model3_2')


def get_spacy_ner(posted_data, nlp_spacy):
    result_dict = {}
    doc = nlp_spacy(posted_data.lower())
    count = 1
    for entity in doc.ents:
        out = {str(count)+str(" ")+entity.label_: entity.text}
        count += 1
        result_dict.update(out)
    return result_dict


def get_resume_ner(posted_data, nlp_resume):
    result_dict = {}
    doc = nlp_resume(posted_data.lower())
    count = 1
    for entity in doc.ents:
        out = {str(count)+str(" ")+entity.label_: entity.text}
        count += 1
        result_dict.update(out)
    return result_dict
