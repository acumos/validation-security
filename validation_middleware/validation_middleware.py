#! python
# -*- coding: utf-8 -*-
# ================================================================================
# ACUMOS
# ================================================================================
# Copyright © 2017 AT&T Intellectual Property & Tech Mahindra. All rights reserved.
# ================================================================================
# This Acumos software file is distributed by AT&T and Tech Mahindra
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ================================================================================
import os
from flask import Flask, jsonify
from flask import request
import requests
import json
import logging
from logging.handlers import RotatingFileHandler
from flask import abort
from flasgger import Swagger
import time

app = Flask(__name__)
swagger = Swagger(app)

# Validation task types = SS, LS, TA, OQ

tasks = []
data = {
    'status': None,
    'artifactValidationStatus': [
        {'artifactTaskId': None,
         'status': None,
         'artifactId': None}
    ],
    'taskId': None
}

# Definition of URLs
URL_PORTAL = os.environ['URL_PORTAL']
URL_TASK_STATUS = os.environ['URL_TASK_STATUS']


# GET verb usage
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


# POST verb usage
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
    virus_id = task['task_details']['virus_task_id']
    license_id = task['task_details']['license_task_id']
    text_search_id = task['task_details']['text_task_id']

    virus_url = '/'.join((URL_TASK_STATUS, 'securityScan', virus_id))
    license_url = '/'.join((URL_TASK_STATUS, 'licenseComp', license_id))
    text_search_url = '/'.join((URL_TASK_STATUS, 'keywordScan', text_search_id))

    q = requests.get(virus_url)
    f = requests.get(license_url)
    z = requests.get(text_search_url)

    virus_object = q.json()
    license_object = f.json()
    text_search_object = z.json()

    base_url2 = (URL_PORTAL, task['task_details']['principle_task_id'])
    new_url2 = '/'.join(base_url2)

    time.sleep(2)
    if virus_object["state"] != "":
        data['status'] = virus_object["status"]
        data['taskId'] = task['task_details']['principle_task_id']
        data['solutionId'] = task['solutionId']
        data['revisionId'] = task['revisionId']
        data['visibility'] = task['visibility']

        data['artifactValidationStatus'][0]['status'] = virus_object["result"]
        data['artifactValidationStatus'][0]['artifactTaskId'] = virus_id
        data['artifactValidationStatus'][0]['artifactId'] = task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType'] = "SS"

        r = requests.put(new_url2, json.dumps(data), headers={"Content-type": "application/json; charset=utf8"})

    time.sleep(3)
    if license_object["state"] != "":
        data['status'] = license_object["status"]
        data['taskId'] = task['task_details']['principle_task_id']
        data['solutionId'] = task['solutionId']
        data['revisionId'] = task['revisionId']
        data['visibility'] = task['visibility']

        data['artifactValidationStatus'][0]['status'] = license_object["result"]
        data['artifactValidationStatus'][0]['artifactTaskId'] = license_id
        data['artifactValidationStatus'][0]['artifactId'] = task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType'] = "LS"

        r = requests.put(new_url2, json.dumps(data), headers={"Content-type": "application/json; charset=utf8"})

    if text_search_object["state"] != "":
        data['status'] = text_search_object["status"]
        data['taskId'] = task['task_details']['principle_task_id']
        data['solutionId'] = task['solutionId']
        data['revisionId'] = task['revisionId']
        data['visibility'] = task['visibility']

        data['artifactValidationStatus'][0]['status'] = text_search_object["result"]
        data['artifactValidationStatus'][0]['artifactTaskId'] = text_search_id
        data['artifactValidationStatus'][0]['artifactId'] = task['artifactValidations'][0]['artifactId']
        data['artifactValidationStatus'][0]['validationTaskType'] = "TA"
        r = requests.put(new_url2, json.dumps(data), headers={"Content-type": "application/json; charset=utf8"})

    return "done", 201


if __name__ == '__main__':
    formatter = logging.Formatter("%(asctime)s | %(pathname)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s")
    logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)
    logHandler.setLevel(logging.DEBUG)
    logHandler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(logHandler)

    app.run(host="0.0.0.0", port=9604, debug=True)
