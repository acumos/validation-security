from flask import Flask, jsonify
from flask import request
import requests
import json
from flask import abort
import uuid
import logging
from logging.handlers import RotatingFileHandler
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Validation task types = SS, LS, TA, OQ
data = {"status": 'Pass', 'artifactValidationStatus': [{'artifactTaskId': '4ab4fcb8-fd91-4885-be7c-163acd683ee7', 'validationTaskType': 'SS',  'status': 'Pass', 'artifactId': '38daf266-cd85-4bb0-a4db-5b3263defa7b'}], 'taskId': '38daf266-cd85-4bb0-a4db-5b3263defa7b','visibility':"PB", 'solutionId':'38daf266-cd85-4bb0-a4db-5b3263defa7b', 'revisionId' : '4ab4fcb8-fd91-4885-be7c-163acd683ee7'}


tasks = []

#GET verb usage
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

#POST verb usage
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():

    if not request.json:
        abort(400)

    task = {
            'solutionId': request.json["solutionId"],
            'revisionId': request.json["revisionId"],
            'visibility': request.json['visibility'],
            'artifactValidations': request.json['artifactValidations'],
            'task_details': request.json["task_details"]
           }
    k = task['task_details']['task_id']
    g = task['task_details']['task_id1']
    p = task['task_details']['task_id2']

    base_url = ('http://root:9605/status',k)
    base_url1 = ('http://root:9605/status',g)
    base_url3 = ('http://root:9605/status',p)

    new_url =  '/'.join(base_url)
    new_url1 =  '/'.join(base_url1)
    new_url3 =  '/'.join(base_url3)

    q = requests.get(new_url)
    f = requests.get(new_url1)
    z = requests.get(new_url3)

    virus_object = q.json()
    license_object = f.json()
    textSearch_object = z.json()

    base_url2 = ('http://acumos-portal-be:8083/validation',task['task_details']['principle_task_id'])
    new_url2 =  '/'.join(base_url2)
#Keyword search

    def json_object():
        l = 'http://cognita-nexus01:8081/repository/repo_cognita_model_maven/com/artifact/word_embeddings_chat_ml_18102017/1.0.0/word_embeddings_chat_ml_18102017-1.0.0.json'
        essential1 = task['artifactValidations']
        for i in essential1:
                if i['artifactName'] == "metadata.json":
                        l= i['url']
        return l
    url_domain = ".eastus.cloudapp.azure.com"
    url_full = json_object()[:22] + url_domain +  json_object()[22:]
    json1 = requests.get(url_full)
    text1 = json1.json()['name']
    dict1 = ['verizon', 'at&t','cognita', 'openai']

    def keyword_search():
        striptext = text1.replace('\n\n', ' ')
        keywords_list = striptext.split()
        keywords_list = [i.lower()for i in keywords_list]
        for j in keywords_list:
                if j in dict1:
                   return ( "FA")
                else:
                   return ("PS")





    if virus_object["state"]!= "":
        data['status']="PS"
        data['taskId']=task['task_details']['principle_task_id']
        data['solutionId']=task['solutionId']
        data['revisionId']=task['revisionId']
        data['visibility']=task['visibility']

        data['artifactValidationStatus'][0]['status']="PS"
        data['artifactValidationStatus'][0]['artifactTaskId']= k
        data['artifactValidationStatus'][0]['artifactId']= task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType']= "SS"

        r = requests.put(new_url2,json.dumps(data),headers={"Content-type":"application/json; charset=utf8"})

    if license_object["state"]!= "":
        data['status']="PS"
        data['taskId']=task['task_details']['principle_task_id']
        data['solutionId']=task['solutionId']
        data['revisionId']=task['revisionId']
        data['visibility']=task['visibility']

        data['artifactValidationStatus'][0]['status']="PS"
        data['artifactValidationStatus'][0]['artifactTaskId']= g
        data['artifactValidationStatus'][0]['artifactId']= task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType']= "LC"

        r = requests.put(new_url2,json.dumps(data),headers={"Content-type":"application/json; charset=utf8"})

    if textSearch_object["state"]!= "":
        data['status']= keyword_search()
        data['taskId']=task['task_details']['principle_task_id']
        data['solutionId']=task['solutionId']
        data['revisionId']=task['revisionId']
        data['visibility']=task['visibility']

        data['artifactValidationStatus'][0]['status']= keyword_search()
        data['artifactValidationStatus'][0]['artifactTaskId']= p
        data['artifactValidationStatus'][0]['artifactId']= task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType']= "TA"
        r = requests.put(new_url2,json.dumps(data),headers={"Content-type":"application/json; charset=utf8"})



    return ("done"), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9604 ,debug=True)

