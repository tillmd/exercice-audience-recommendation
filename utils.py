# encoding: UTF-8

from itertools import combinations
from collections import defaultdict
import json
import numpy as np
import operator
import pandas as pd
from user import User


def load_data():
    with open('data/users.json') as json_data:
        d = json.load(json_data)
    return d


def get_cooccurrence(users, field='artist', min_score=0):
    d = defaultdict(int)
    for user in users:
        artists = sorted(
            [track[field] for track in user.tracks if track['score'] > min_score])
        for pair in combinations(artists, 2):
            d[pair] += 1
    return d


def get_top_cooccurrence(users, field='artist', min_score=0, limit=20):
    d = get_cooccurrence(users, field, min_score)
    return [list(k) + [d[k]] for k in sorted(d, key=d.get, reverse=True)[:limit]]


def get_scores(users, field, rounding=False):
    scores = {}
    for user in users:
        for track in user.tracks:
            score = track['score']
            if rounding:
                score = np.round_(track['score'], 2)
            if track[field] in scores:
                scores[track[field]] += [score]
            else:
                scores[track[field]] = [score]
    return scores


def get_mean_popularity(users, field):
    scores = get_scores(users, field)
    mean_scores = {key: np.mean(value) for (key, value) in scores.iteritems()}
    return sorted(mean_scores.items(), key=operator.itemgetter(1), reverse=True)


def get_distinct(users, field):
    return len(
        set(
            sum(
                [list(set(pd.DataFrame(user.tracks)[field])) for user in users]
                , [])
            )
        )


def get_counts(users, field):
    return pd.DataFrame(
        sum([user.tracks for user in users], [])
    ).groupby(field).size()
