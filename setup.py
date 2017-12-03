from setuptools import setup, find_packages 
 

 
setup(name='validation-security', 
      version='1.0.0', 
      description='This is a cool microservice for validation and security.', 
      author='Duwarahan Rajendra', 
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