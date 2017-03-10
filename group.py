# encoding: UTF-8

from collections import Counter
import pandas as pd
from user import User
from utils import get_top_cooccurrence


class Group(object):

    def __init__(self, users):
        self.users = users
        self.tracklisting = self.get_field_listing("id")
        self.common_tracks = self.count_common_field("id")

    def get_field_listing(self, field):
        return set(dict(self.get_field_count(field)).keys())

    def count_common_field(self, field):
        tracks_count = self.get_field_count(field)
        return Counter(tracks_count.values())

    def get_field_count(self, field):
        tracks = sum(
            [list(
                    set([track[field] for track in user.tracks])
            ) for user in self.users],
            [])
        return Counter(tracks)

    def get_cooccurences(self, min_score, field):
        tracks_cooccurrence = get_top_cooccurrence(
            self.users,
            field=field,
            min_score=min_score,
            limit=len(self.tracklisting))
        cooccurrence = pd.DataFrame(
            tracks_cooccurrence, columns=['t1', 't2', 'count'])
        r_cooccurrence = pd.DataFrame(
            tracks_cooccurrence, columns=['t2', 't1', 'count'])
        return pd.concat([cooccurrence, r_cooccurrence], ignore_index=True)

    def user_without_track(self, track_id, field):
        for user in self.users:
            if track_id not in [t[field] for t in user.tracks]:
                return user

    def get_similar(self, cooccurrences, track):
        coocur = cooccurrences[cooccurrences.t1 == track]
        return (track, list(coocur.sort_values(by='count', ascending=0).t2))

    def make_reco(self, min_score, field):
        nb_users = len(self.users)
        cooccurrences = self.get_cooccurences(min_score, field)
        counts = self.count_common_field(field).keys()
        field_count = self.get_field_count(field).iteritems()
        field_listing = set(self.get_field_listing(field)

        for i in sorted(counts, reverse=True)[:-1]:
            common_track_ids = {
                key: value for (key, value) in field_count if value == i
            }.keys()
            short_list = [
                self.get_similar(cooccurrences, track) for track in common_track_ids
            ]
            res = []
            for track_id, cooccur_track in short_list:
                allowed_tracks = self.user_without_track(track_id, field).tracks
                if i == nb_users:
                    res.append((track_id, set(cooccur_track) - field_listing)))
                else:
                    allowed_track_id = set([t[field] for t in allowed_tracks])
                    res.append(
                        (
                            track_id,
                            set(cooccur_track) - (field_listing - allowed_track_id))
                        )
        return pd.DataFrame(res)

    def count_common_genres(self):
        pass

    def count_common_artists(self):
        pass

    def get_top_common_tracks(self):
        pass

    def get_top_common_artists(self):
        pass

    def get_affinity_score(self):
        pass
