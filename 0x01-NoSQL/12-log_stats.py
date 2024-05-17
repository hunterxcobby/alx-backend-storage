#!/usr/bin/env python3

"""a Python script that provides some
stats about Nginx logs stored in MongoDB"""


from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    all_logs = collection.count_documents({})
    get_logs = collection.count_documents({"method": "GET"})
    post_logs = collection.count_documents({"method": "POST"})
    put_logs = collection.count_documents({"method": "PUT"})
    patch_logs = collection.count_documents({"method": "PATCH"})
    delete_logs = collection.count_documents({"method": "DELETE"})
    checks = collection.count_documents({"method": "GET", "path": "/status"})

    print("{} logs\n Methods:\n \t  method GET: {} \n\t  method POST: {} \n\t  method"
          " PUT: {} \n\t  method PATCH: {} \n\t  method DELETE: {}"
          "\n status_checks: {}".format(all_logs, get_logs, post_logs, put_logs, patch_logs, delete_logs, checks))
