from pymongo import MongoClient


def connect_database():
    cluster = MongoClient(
        'mongodb+srv://IgnacioRamos:TZxa68aDGrWWVUeq@cluster0.tzlxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
        )
    db = cluster['password_manager']
    collection = db['accounts']

    return collection
