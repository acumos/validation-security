from flask import Flask, jsonify
from flask import request
import requests
import json
from flask import abort
import uuid

app = Flask(__name__)

# Validation task types = SS, LS, TA, OQ

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

    base_url = (URL_TASK_STATUS,k)
    base_url1 = (URL_TASK_STATUS,g)
    base_url3 = (URL_TASK_STATUS,p)

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

    if virus_object["state"]== "SUCCESS":
        data['status']=virus_object["result"]
        data['taskId']=task['task_details']['principle_task_id']
        data['solutionId']=task['solutionId']
        data['revisionId']=task['revisionId']
        data['visibility']=task['visibility']

        data['artifactValidationStatus'][0]['status']=virus_object["result"]
        data['artifactValidationStatus'][0]['artifactTaskId']= k
        data['artifactValidationStatus'][0]['artifactId']= task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType']= "SS"

        r = requests.put(new_url2,json.dumps(data),headers={"Content-type":"application/json; charset=utf8"})

    if license_object["state"]== "SUCCESS":
        data['status']=license_object["result"]
        data['taskId']=task['task_details']['principle_task_id']
        data['solutionId']=task['solutionId']
        data['revisionId']=task['revisionId']
        data['visibility']=task['visibility']

        data['artifactValidationStatus'][0]['status']=license_object["result"]
        data['artifactValidationStatus'][0]['artifactTaskId']= g
        data['artifactValidationStatus'][0]['artifactId']= task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType']= "LS"

        r = requests.put(new_url2,json.dumps(data),headers={"Content-type":"application/json; charset=utf8"})

    if textSearch_object["state"]== "SUCCESS":
        data['status']=textSearch_object["result"]
        data['taskId']=task['task_details']['principle_task_id']
        data['solutionId']=task['solutionId']
        data['revisionId']=task['revisionId']
        data['visibility']=task['visibility']

        data['artifactValidationStatus'][0]['status']=textSearch_object["result"]
        data['artifactValidationStatus'][0]['artifactTaskId']= p
        data['artifactValidationStatus'][0]['artifactId']= task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType']= "TA"
        r = requests.put(new_url2,json.dumps(data),headers={"Content-type":"application/json; charset=utf8"})



    return ("done"), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9604 ,debug=True)

