import os
# HOSTNAME example: "http://localhost:8000/" - necessarily end with "/"
# MONGO_HOST example: "mongodb://myuser:mypass@db:27017/" - "db" is the name of the container
# DEBUG example: True or False if you want to use debug mode

HOSTNAME = "http://localhost:8000/"
MONGO_HOST = f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@db:27017/"
DEBUG = True
MONGO_HOST = "mongodb://localhost:27017/"
