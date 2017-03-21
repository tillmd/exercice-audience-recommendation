# encoding: UTF-8

from group import Group
import pandas as pd
from user import User
from utils import get_top_cooccurrence


class RecoEngine(object):

    def __init__(self, group):
        self.group = group
        self.users = group.users
        self.init_tracks_db()
        pass

    def init_tracks_db(self):
        self.tracks_db = pd.DataFrame(
            sum([user.tracks for user in self.users], []))
        self.tracks_db = self.tracks_db.groupby(
            ['id', 'artist', 'genre']).mean()
        self.tracks_db = self.tracks_db.reset_index()
        self.tracks_db = self.tracks_db.set_index("id")

        self.artists_db = self.tracks_db.groupby(
            ['artist']).mean()
        self.db = dict()
        self.db['id'] = self.tracks_db
        self.db['artist'] = self.artists_db

    def get_cooccurences(self, min_score, field):
        tracks_cooccurrence = get_top_cooccurrence(
            self.users,
            field=field,
            min_score=min_score,
            limit=len(self.group.tracklisting))
        cooccurrence = pd.DataFrame(
            tracks_cooccurrence, columns=['t1', 't2', 'count'])
        r_cooccurrence = pd.DataFrame(
            tracks_cooccurrence, columns=['t2', 't1', 'count'])
        return pd.concat([cooccurrence, r_cooccurrence], ignore_index=True)

    def make_reco(self, min_score, field):
        cooccurrence = self.get_cooccurences(min_score, field)

        res = []
        common_field_count = self.group.count_common_field(field).keys()
        # Iteration on most shared field values
        for i in sorted(common_field_count, reverse=True)[:-1]:
            common_track_ids = {
                key: val
                for (key, val) in self.group.get_field_count(field).iteritems()
                if val == i and self.db[field].loc[key].score >= min_score
            }.keys()
            short_list = [(
                track,
                list(cooccurrence[cooccurrence.t1 == track].sort_values(
                    by='count', ascending=0).t2)
                )
                for track in common_track_ids]

            res += self.short_list_reco(i, field, short_list)

        return pd.DataFrame(res, columns=["nb_common_user", field, "reco"])

    def short_list_reco(self, i, field, short_list):
        res = []
        for track_id, cooccur_track in short_list:
            # If everyone share the field value
            # the keep this value
            if i == len(self.users):
                if field == "id":
                    track = self.tracks_db.loc[track_id]
                    res.append((i, track_id, track['score']))
                else:
                    artist_song = self.tracks_db[self.tracks_db.artist == track_id]
                    score = artist_song.score.mean()
                    res.append((i, track_id, score))
            # Else
            # use relevant cooccurrence and allow to find it
            # in the user who had not the common track
            else:
                allowed_track_id = set([
                        t[field]
                    for t in self.group.user_without_track(track_id, field).tracks
                ])
                res.append((
                    i,
                    track_id,
                    set(cooccur_track) - (set(self.group.get_field_listing(field)) - allowed_track_id))
                )

        return res
