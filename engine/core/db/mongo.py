import pymongo


class MongoTestDrive:

    def __init__(self):
        client = pymongo.MongoClient("mongodb://googigg:024545055@cluster0-shard-00-00-3i0ff.mongodb.net:27017,cluster0-shard-00-01-3i0ff.mongodb.net:27017,cluster0-shard-00-02-3i0ff.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
        db = client.test

