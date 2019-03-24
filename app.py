from flask import Flask, request, render_template, jsonify, flash, redirect,url_for
import uuid
import re
import datetime
from utils import clean_text, col, counttokens
from ner import get_spacy_ner, get_resume_ner, nlp_spacy, nlp_resume
from topic_modelling import get_topic_modelling
from logging_utils import setup_logging_to_file, log_exception
import logging
# import bcrypt

app = Flask(__name__)
app.secret_key = 'random string'


@app.route('/token_end_flash')
def token_end_flash():
    return render_template("spacy/spacy_trials.html")


@app.route('/')
def index():
    visitor_info = request.environ
    visitor_ip = visitor_info.get('REMOTE_ADDR')
    visitor_device = (visitor_info.get('HTTP_USER_AGENT').split(')')[0]).split(';')[-1].strip()
    visitor_username = "hsengivnlp"+".".join(visitor_ip.split('.')[0:3])+visitor_device
    # hashed_pw = bcrypt.hashpw(visitor_pass.encode('utf8'), bcrypt.gensalt())
    query = col.count_documents({"Username": str(visitor_username)})
    try:
        if query == 0:
            col.insert({
                "Username": str(visitor_username),
                "visitor_device": str(visitor_device),
                "visitor_mac": ':'.join(re.findall('..', '%012x' % uuid.getnode())),
                "visitor_addr": str(visitor_ip),
                "others": str(visitor_info),
                "tokens": 10,
                "date":datetime.datetime.today()
            })
        return render_template("index.html")
    except Exception as e:
        logging.exception("** AT END POINT / **")
        log_exception(e)
        ret_json = {'status': 500, 'message': 'internal server error'}
        return jsonify(ret_json)


@app.route('/smodelIn')
def smodel_in():
    visitor_info = request.environ
    visitor_ip = visitor_info.get('REMOTE_ADDR')
    visitor_device = (visitor_info.get('HTTP_USER_AGENT').split(')')[0]).split(';')[-1].strip()
    visitor_username = "hsengivnlp"+".".join(visitor_ip.split('.')[0:3])+visitor_device
    try:
        avail_tokens = counttokens(visitor_username)
        if avail_tokens > 0:
            col.update({"Username": visitor_username},
                      {"$set": {"tokens": avail_tokens - 1, "date": datetime.datetime.today()}})
            return render_template("spacy/spacy_input.html")
        else:
            flash("Sorry trials exceeded")
            return redirect(url_for('token_end_flash'))
            # return render_template("spacy/spacy_trials.html")
    except Exception as e:
        logging.exception("** AT END POINT /getDetails **")
        log_exception(e)
        ret_json = {'status': 500, 'message': 'internal server error'}
        return jsonify(ret_json)


@app.route('/smodelOut', methods=['post'])  # en_core_web_sm
def smodel_out():
    visitor_info = request.environ
    visitor_ip = visitor_info.get('REMOTE_ADDR')
    visitor_device = (visitor_info.get('HTTP_USER_AGENT').split(')')[0]).split(';')[-1].strip()
    visitor_username = "hsengivnlp"+".".join(visitor_ip.split('.')[0:3])+visitor_device
    try:
        avail_tokens = counttokens(visitor_username)
        if avail_tokens > 0:
            col.update({"Username": visitor_username},
                       {"$set": {"tokens": avail_tokens - 1, "date": datetime.datetime.today()}})
            posted_data = request.form.get('sample_text')
            result_dict = get_spacy_ner(posted_data, nlp_spacy)
            return render_template("spacy/spacy_output.html", result=result_dict)
        else:
            flash("Sorry trials exceeded")
            return redirect(url_for('token_end_flash'))
            # return render_template("spacy/spacy_trials.html")
    except Exception as e:
        logging.exception("** AT END POINT /getDetails **")
        log_exception(e)
        ret_json = {'status': 500, 'message': 'internal server error'}
        return jsonify(ret_json)


@app.route('/rmodelIn')
def rmodel_in():
    visitor_info = request.environ
    visitor_ip = visitor_info.get('REMOTE_ADDR')
    visitor_device = (visitor_info.get('HTTP_USER_AGENT').split(')')[0]).split(';')[-1].strip()
    visitor_username = "hsengivnlp"+".".join(visitor_ip.split('.')[0:3])+visitor_device
    try:
        avail_tokens = counttokens(visitor_username)
        if avail_tokens > 0:
            col.update({"Username": visitor_username},
                       {"$set": {"tokens": avail_tokens - 1, "date": datetime.datetime.today()}})
            return render_template("resume/resume_input.html")
        else:
            flash("Sorry trials exceeded")
            return redirect(url_for('token_end_flash'))
    except Exception as e:
        logging.exception("** AT END POINT /getDetails **")
        log_exception(e)
        ret_json = {'status': 500, 'message': 'internal server error'}
        return jsonify(ret_json)


@app.route('/rmodelOut', methods=['post'])
def rmodel_out():
    result_dict = {}
    visitor_info = request.environ
    visitor_ip = visitor_info.get('REMOTE_ADDR')
    visitor_device = (visitor_info.get('HTTP_USER_AGENT').split(')')[0]).split(';')[-1].strip()
    visitor_username = "hsengivnlp"+".".join(visitor_ip.split('.')[0:3])+visitor_device
    try:
        avail_tokens = counttokens(visitor_username)
        if avail_tokens > 0:
            col.update({"Username": visitor_username},
                       {"$set": {"tokens": avail_tokens - 1, "date": datetime.datetime.today()}})
            posted_data = request.form.get('sample_text')
            result_dict = get_resume_ner(posted_data, nlp_resume)
            return render_template("resume/resume_output.html", result=result_dict)
        else:
            flash("Sorry trials exceeded")
            return redirect(url_for('token_end_flash'))
    except Exception as e:
        logging.exception("** AT END POINT /getDetails **")
        log_exception(e)
        ret_json = {'status': 500, 'message': 'internal server error'}
        return jsonify(ret_json)


@app.route('/tmodelIn')
def tmodel_in():
    visitor_info = request.environ
    visitor_ip = visitor_info.get('REMOTE_ADDR')
    visitor_device = (visitor_info.get('HTTP_USER_AGENT').split(')')[0]).split(';')[-1].strip()
    visitor_username = "hsengivnlp"+".".join(visitor_ip.split('.')[0:3])+visitor_device
    try:
        avail_tokens = counttokens(visitor_username)
        if avail_tokens > 0:
            col.update({"Username": visitor_username},
                       {"$set": {"tokens": avail_tokens - 1, "date": datetime.datetime.today()}})
            return render_template("topic_modelling/topic_input.html")
        else:
            flash("Sorry trials exceeded")
            return redirect(url_for('token_end_flash'))
    except Exception as e:
        logging.exception("** AT END POINT /getDetails **")
        log_exception(e)
        ret_json = {'status': 500, 'message': 'internal server error'}
        return jsonify(ret_json)


@app.route('/tmodelOut', methods=['post'])
def tmodel_out():
    count = 1
    top = {}
    # result_dict = {}
    visitor_info = request.environ
    visitor_ip = visitor_info.get('REMOTE_ADDR')
    visitor_device = (visitor_info.get('HTTP_USER_AGENT').split(')')[0]).split(';')[-1].strip()
    visitor_username = "hsengivnlp"+".".join(visitor_ip.split('.')[0:3])+visitor_device
    try:
        avail_tokens = counttokens(visitor_username)
        if avail_tokens > 0:
            col.update({"Username": visitor_username},
                       {"$set": {"tokens": avail_tokens - 1}})
            posted_data = request.form.get('sample_text')
            avg_posted_data = len(clean_text(posted_data).split())
            # print('avg_posted_data:', avg_posted_data)
            try:
                no_of_topics = int(request.form.get('no_of_topics'))
            except Exception as e:
                logging.exception("** AT END POINT /getDetails **")
                log_exception(e)
                no_of_topics = 1
            top = get_topic_modelling(posted_data,
                                      no_of_topics,
                                      avg_posted_data,
                                      count=1)
            return render_template("topic_modelling/topic_output.html", result=top, message=None)
        else:
            flash("Sorry trials exceeded")
            return redirect(url_for('token_end_flash'))
    except Exception as e:
        logging.exception("** AT END POINT /getDetails **")
        log_exception(e)
        ret_json = {'status': 500, 'message': 'internal server error'}
        return jsonify(ret_json)


@app.route('/textClassifyHome')
def text_classify_home():
    return render_template("text_classify/text_classify_index.html")


@app.route('/spellCorrectIn')
def spell_correct_in():
    return render_template("spell_correction/input.html")


if __name__ == '__main__':
    setup_logging_to_file("app.log")
    app.run('0.0.0.0', debug=True)


#
