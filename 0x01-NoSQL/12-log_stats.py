#!/usr/bin/env python3
import pymongo
"""
12-log_stats module
"""


def log_nginx_stats(mongo_collection):
    """provides some stats about Nginx logs"""
    print(f"{mongo_collection.estimated_document_count()} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    number_of_gets = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{number_of_gets} status check")


if __name__ == "__main__":
    """
    main program
    """
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client['logs']
    collection = db['nginx']

    # Call the logs_stats function
    log_nginx_stats(collection)
