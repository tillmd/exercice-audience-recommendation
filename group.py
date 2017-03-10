# encoding: UTF-8

from collections import Counter
from user import User


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

    def user_without_track(self, track_id, field):
        for user in self.users:
            if track_id not in [t[field] for t in user.tracks]:
                return user
