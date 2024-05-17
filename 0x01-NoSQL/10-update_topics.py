#!/usr/bin/env python3

""" Module with function that changes all the topics of a school document
based on the name.
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name.

    Args:
        mongo_collection: pymongo collection object.
        name (str): The school name to update.
        topics (list of str): The list of topics approached in the school.

    Returns:
        None
    """
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
