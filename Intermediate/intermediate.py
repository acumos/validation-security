from flask import Flask, jsonify
from flask import request
import requests
import json
from flask import abort
import uuid
from flasgger import Swagger
import time
import logging
import os
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
swagger = Swagger(app)

# Validation task types = SS, LC, TA, OQ
data = {"status": 'Pass', 'artifactValidationStatus': [{'artifactTaskId': '4ab4fcb8-fd91-4885-be7c-163acd683ee7', 'validationTaskType': 'SS',  'status': 'Pass', 'artifactId': '38daf266-cd85-4bb0-a4db-5b3263defa7b'}], 'taskId': '38daf266-cd85-4bb0-a4db-5b3263defa7b','visibility':"PB", 'solutionId':'38daf266-cd85-4bb0-a4db-5b3263defa7b', 'revisionId' : '4ab4fcb8-fd91-4885-be7c-163acd683ee7'}


tasks = []

# Definition of URL's
URL_PORTAL = os.environ['url1']
URL_CCDS = os.environ['url2']
URL_NEXUS = os.environ['url3']



#GET verb usage
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

#POST verb usage
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():

    """
    This is an example
    ---
    tags:
      - restful
    parameters:
      - in: body
        name: body
        schema:
          $ref: '#/definitions/Task'
    responses:
       201:
        description: The task has been created
        schema:
          $ref: '#/definitions/Task'
    """






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

    base_url2 = (URL_PORTAL,task['task_details']['principle_task_id'])
    new_url2 =  '/'.join(base_url2)

#Defining the parsed json object
    def json_object():
	l = URL_NEXUS
    	essential1 = task['artifactValidations']
    	for i in essential1:
        	if i['artifactName'] == "metadata.json":
            		l= i['url']  
    	return l
    json1 = requests.get(json_object())
    text1 = json1.json()['name']
    text2 = json1.json()['runtime']

#Realtime site config
    url_info = requests.get(URL_CCDS,auth=('ccds_client', 'ccds_client'))
    data1 = json.loads(url_info.json()['configValue'])['fields'][-1]['data'].encode()
#temperory database in a listshape
    dict1 = []
    dict1.append(data1)
    dict_security = ['PyYAML']
    dict_license = ['happyml']

#Keyword search

    def keyword_search():
    	striptext = text1.replace('\n\n', ' ')
    	keywords_list = striptext.split()
    	keywords_list = [i.lower()for i in keywords_list]
    	for j in keywords_list:           
       		if j in dict1:
          	   return ( "FA")
       		else:
          	   return ("PS")

#Doing license check
    def license_check():
	license_list = []
        license12 = text2['dependencies']['pip']['requirements']
	for j in license12:
	    license_list.append(j['name'])
        for i in dict_license:
	   
                if i in license_list:
                   return ( "FA")
                else:
                   return ("PS")

#Doing Secuirty check
    def security_check():
	security_list = []
        security12 = text2['dependencies']['pip']['requirements']
        for j in security12:
            security_list.append(j['name'])

        for i in dict_security:
                if i in security_list:
                   return ( "FA")
                else:
                   return ("PS")









    time.sleep(2)
    if virus_object["status"]!= "":
        data['status']= security_check()
        data['taskId']=task['task_details']['principle_task_id']
        data['solutionId']=task['solutionId']
        data['revisionId']=task['revisionId']
        data['visibility']=task['visibility']

        data['artifactValidationStatus'][0]['status']=security_check()
        data['artifactValidationStatus'][0]['artifactTaskId']= k
        data['artifactValidationStatus'][0]['artifactId']= task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType']= "SS"

        r = requests.put(new_url2,json.dumps(data),headers={"Content-type":"application/json; charset=utf8"})
    time.sleep(3)
    if license_object["status"]!= "":
        data['status']= license_check()
        data['taskId']=task['task_details']['principle_task_id']
        data['solutionId']=task['solutionId']
        data['revisionId']=task['revisionId']
        data['visibility']=task['visibility']

        data['artifactValidationStatus'][0]['status']= license_check()
        data['artifactValidationStatus'][0]['artifactTaskId']= g 
        data['artifactValidationStatus'][0]['artifactId']= task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType']= "LC"

        r = requests.put(new_url2,json.dumps(data),headers={"Content-type":"application/json; charset=utf8"})

    if textSearch_object["status"]!= "":
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


    return ("Done"), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9604 ,debug=True)

