from collections import defaultdict


def groupby(iterable, projection):
    result = defaultdict(list)
    for item in iterable:
        result[projection(item)].append(item)
    return dict(result)
