# encoding: UTF-8

import numpy as np
from collections import Counter


class User():

    """docstring for User"""
    def __init__(self, id, tracks):
        self.id = id
        self.tracks = tracks
        self.compute_hipster_score()

    def get_mean_score(self):
        return np.mean([track['score'] for track in self.tracks])

    def get_mean_score(field):
        res = {}
        for track in self.tracks:
            if track[field] in res:
                res[track[field]] += [track['score']]
            else:
                res[track[field]] = [track['score']]
        return {key: np.mean(value) for (key, value) in res.iteritems()}

    def get_score_distribution(self):
        return Counter([round(track['score'], 1) for track in self.tracks])

    def get_std(self):
        # On suppose que qqn de picky aura bcp de mauvaises et hautes notes
        return np.std([track['score'] for track in self.tracks])

    def compute_hipster_score(self):
        # Not implemented
        self.hipster_code = 0.0
        pass

    def get_top_tracks(self, limit=5):
        return sorted(self.tracks, key=lambda k: k['id'], reverse=True)[:limit]
