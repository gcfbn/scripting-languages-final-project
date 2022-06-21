from collections import defaultdict


def groupby(iterable, projection):
    """
    Group an iterable by a projection.
    :param iterable: Collection of values containing common property.
    :param projection: Function that returns a value to group by.
    :return: Dictionary of list of values grouped by the projection.
    """
    result = defaultdict(list)
    for item in iterable:
        result[projection(item)].append(item)
    return dict(result)
