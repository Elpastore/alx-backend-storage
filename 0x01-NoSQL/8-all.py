#!/usr/bin/env python3
"""
8-all module
"""
import pymongo


def list_all(mongo_collection):
    """
    function that lists all documents in a collection
    """
    if mongo_collection is None:
        return []
    all_documents = mongo_collection.find()
    return [document for document in all_documents]
