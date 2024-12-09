from pymongo import MongoClient


class NoSqlDB:
    def __init__(self, db_config):
        """
        docker run --name mongodb -d -p 27017:27017 mongo
        """
        mongo_uri = db_config["mongo_uri"]
        db_name = db_config["db_name"]
        collection_name = db_config["collection_name"]
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.collection.create_index("url", unique=True)

    def insert(self, url, document):
        if self.collection.find_one({"url": url}):
            return False
        document = {**document, "url": url}
        self.collection.insert_one(document)
        return True

    def find(self, url):
        document = self.collection.find_one({"url": url})
        if not document:
            return None
        return document
    
    def find_all(self):
        return self.collection.find({})

    def delete(self, url):
        return self.collection.delete_one({"url": url})

    def delete_all(self):
        return self.collection.delete_many({})
