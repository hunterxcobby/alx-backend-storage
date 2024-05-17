#!/usr/bin/env python3

""" Module with script to get the list of school having a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """
    Python function that returns the list of school
    having a specific topic.
    """
    doc_list = mongo_collection.find(
        {"topics": topic}
        )
    return [doc for doc in doc_list]
