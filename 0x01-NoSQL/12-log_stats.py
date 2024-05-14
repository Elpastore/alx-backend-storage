#!/usr/bin/env python3
import pymongo


def logs_stats(collection):
    """
    Provides some stats about Nginx logs stored in MongoDB.
    """
    # Calculate total number of log entries
    logs = collection.count_documents({})
    print(f"{logs} logs")

    # List of HTTP methods to count
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        # Count documents with each HTTP method
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count documents with method=GET and path=/status
    status_count = collection.count_documents({"method": "GET",
                                               "path": "/status"})
    print(f"{status_count} status check")


if __name__ == "__main__":
    """
    main program
    """
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['logs']
    collection = db['nginx']

    # Call the logs_stats function
    logs_stats(collection)

    # Close the MongoDB connection
    client.close()
