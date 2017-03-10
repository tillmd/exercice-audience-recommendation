# encoding: UTF-8

import pandas as pd


class RankingEngine(object):

    def __init__(self, reco_engine):
        self.reco_engine = reco_engine
        self.users = self.reco_engine.group.users

    def get_score(self, track_id):
        return self.reco_engine.tracks_db.loc[track_id].score

    def get_top_tracks_per_artist(self, artist, min_score=None):
        if min_score:
            return self.reco_engine.tracks_db[
            (self.reco_engine.tracks_db.artist == artist) &
            (self.reco_engine.tracks_db.artist == min_score)]
        else:
            return self.reco_engine.tracks_db[self.reco_engine.tracks_db.artist == artist]

    def add_marker(self, title, index):
        return pd.DataFrame({
            "artist": title,
            "genre": "----",
            "score": 0
            }, index=[index])

    def add_first_tracks(self, res, min_score):
        nb_users = len(self.users)
        reco_tracks = self.reco_engine.make_reco(min_score, "id")
        
        # Shared by everyone
        res = pd.concat([res, self.add_marker('First', 1)])
        best_tracks = list(reco_tracks[reco_tracks.nb_common_user == nb_users].sort_values(by="reco", ascending=False).id)
        res = pd.concat([res, self.reco_engine.tracks_db.loc[best_tracks]])

        # Share by more than 1 user
        res = pd.concat([res, self.add_marker('FirstFirst', 11)])
        second_best = reco_tracks[reco_tracks.nb_common_user != nb_users]
        second_best_list = list(second_best.id)
        second_best_df =  self.reco_engine.tracks_db.loc[second_best_list].reset_index().merge(second_best, on="id")
        second_best_list =  list(second_best_df.sort_values(by=['nb_common_user', 'score'], ascending=False).id)
        filtered_second_best = self.reco_engine.tracks_db.loc[second_best_list]
        filtered_second_best = filtered_second_best[filtered_second_best.score >= min_score]
        res = pd.concat([res, filtered_second_best])
        return res, second_best

    def add_second_tracks(self, res, second_best):
        # Second: the correlated song with a score equal to the seed track score times the track mean score
        res = pd.concat([res, self.add_marker('Second', 2)])
        reco_tracks = []
        for i, row in second_best.iterrows():
            track_score = self.get_score(row.id)
            reco_tracks.append([(row.nb_common_user, track_score, track_id, self.get_score(track_id)) for track_id in row.reco])

        reco_tracks_df =  pd.DataFrame(sum(reco_tracks, []), columns=['common_users', 'seed_track_score', 'track_id', 'track_score'])
        reco_tracks_df['score'] = reco_tracks_df['seed_track_score'] * reco_tracks_df['track_score']
        reco_tracks_list = list(reco_tracks_df.sort_values(by=['common_users', 'score'], ascending=False).track_id)
        res = pd.concat([res, self.reco_engine.tracks_db.loc[reco_tracks_list]])
        return res

    def add_third_tracks_1(self, res, min_score):
        nb_users = len(self.users)
        res = pd.concat([res, self.add_marker('Third', 3)])
        #    + First for the artist known by everybody
        reco_artist = self.reco_engine.make_reco(min_score, "artist")
        filtering = (reco_artist.nb_common_user == nb_users) & (reco_artist.reco >= min_score)
        selected_artists = reco_artist[filtering]
        third_df = pd.DataFrame()
        for i, row in selected_artists.iterrows():
            tracks = self.get_top_tracks_per_artist(row.artist)
            tracks.score = tracks.score * row.nb_common_user
            third_df = pd.concat([third_df, tracks])

        third_list = list(third_df.sort_values(by="score").index)
        res = pd.concat([res, self.reco_engine.tracks_db.loc[third_list]])
        return reco_artist, res

    def add_third_tracks_2(self, res, min_score, reco_artist):
        nb_users = len(self.users)
        #    + Second less shares artist
        #    Get mean score of each artist
        res = pd.concat([res, self.add_marker('ThirdThird', 33)])
        filtering = (reco_artist.nb_common_user != nb_users)
        selected_artists = reco_artist[filtering]
        selected_artists['score'] = selected_artists.artist.apply(lambda x: self.get_top_tracks_per_artist(x).score.mean())
        selected_artists = selected_artists[selected_artists.score >= min_score]
        third_df = pd.DataFrame()
        for i, row in selected_artists.iterrows():
            tracks = self.get_top_tracks_per_artist(row.artist)
            tracks.score = tracks.score * row.nb_common_user
            third_df = pd.concat([third_df, tracks])

        third_list = list(third_df.sort_values(by="score").index)
        res = pd.concat([res, self.reco_engine.tracks_db.loc[third_list]])
        return res

    def add_third_tracks_3(self, res, min_score, reco_artist):
        nb_users = len(self.users)
        #    + Finally correlated artist songs still above a min score (in average)
        res = pd.concat([res, self.add_marker('ThirdThirdThird', 333)])
        last_selected_artists = set([])

        filtering = (reco_artist.nb_common_user != nb_users)
        selected_artists = reco_artist[filtering]
        for i, row in  selected_artists.iterrows():
            [last_selected_artists.add(artist) for artist in row.reco]

        last_selected_artists = last_selected_artists - set(list(selected_artists.artist))

        last_selected_artists_df = pd.DataFrame()
        for i in last_selected_artists:
            last_selected_artists_df = pd.concat([last_selected_artists_df, self.get_top_tracks_per_artist(i)])

        last_selected_artists_list = list(last_selected_artists_df[last_selected_artists_df.score >= min_score].index)
        res = pd.concat([res, self.reco_engine.tracks_db.loc[last_selected_artists_list]])
        return res

    def add_third_tracks(self, res, min_score):
        # - Third: the songs by the common artist with a mean score above a "min score"
        reco_artist, res = self.add_third_tracks_1(res, min_score)
        res = self.add_third_tracks_2(res, min_score, reco_artist)
        res = self.add_third_tracks_3(res, min_score, reco_artist)
        return res

    def make_ranking(self, min_score):
        nb_users = len(self.users)
        res = pd.DataFrame()

        res, second_best = self.add_first_tracks(res, min_score)
        res = self.add_second_tracks(res, second_best)
        res = self.add_third_tracks(res, min_score)

        # print "Last"
        res = pd.concat([res, pd.DataFrame({
            "artist": "Last",
            "genre": "----",
            "score": 0
            }, index=[4])])

        last_ids = list(self.reco_engine.group.tracklisting - set(res.index))
        res = pd.concat([res, self.reco_engine.tracks_db.loc[last_ids].sort_values(by='score', ascending=False)])

        return res.drop_duplicates()