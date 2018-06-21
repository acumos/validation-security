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
from setuptools import setup, find_packages
 

 
setup(name='validation-security', 
      version='1.0.0', 
      description='This is a cool microservice for validation and security.', 
      install_requires= ['Flask',
                         'Flask-Mail',
                         'Jinja2',
                         'MarkupSafe',
                          'Werkzeug',
                          'amqp',
                          'anyjson',
                          'argparse',
                          'billiard',
                          'blinker',
                          'celery',
                          'itsdangerous',
                          'kombu',
                          'pytz',
                          'redis',
                          'requests',
                          'flasgger']
      
    ) 