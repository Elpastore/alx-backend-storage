#!/usr/bin/env python3
"""Write a Python script that provides some stats about Nginx
logs stored in MongoDB:
"""
import pymongo
from pymongo import MongoClient


def nginx_logs_stats(collection):
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    # Total number of log entries
    total_logs = collection.estimated_document_count()
    print(f"{total_logs} logs")

    # Number of documents with each HTTP method
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in http_methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Number of documents with method=GET and path=/status
    status_count = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_count} status check")

    # IP
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ten = collection.aggregate(pipeline)
    print('IPs:')
    for ip in top_ten:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client.logs
    collection = db.nginx

    # Call nginx_logs_stats function
    nginx_logs_stats(collection)
