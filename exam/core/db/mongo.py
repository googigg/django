import pymongo
import datetime

class MongoTestDrive:

    posts = None

    def __init__(self):
        print('[MongoTestDrive][init]')

        client = pymongo.MongoClient("mongodb://googigg:024545054@cluster0-shard-00-00-3i0ff.mongodb.net:27017,cluster0-shard-00-01-3i0ff.mongodb.net:27017,cluster0-shard-00-02-3i0ff.mongodb.net:27017/<DATABASE>?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
        # db = client.test
        db = client['test-database']

        self.posts = db.posts

    def add(self):
        post = { "author": "Mike",
                 "text": "My first blog post!",
                 "tags": ["mongodb", "python", "pymongo"],
                 "date": datetime.datetime.utcnow() }

        post_id = self.posts.insert_one(post).inserted_id
        post_id

print('hello')
# m = MongoTestDrive()
# m.add()