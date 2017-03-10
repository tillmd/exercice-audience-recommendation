# encoding: UTF-8

from utils import *
from user import User
from nose.tools import *
import unittest
from unittest import TestCase


class TestUtils(TestCase):

    def setUp(self):
        track1 = {
            "artist": "Doc Gyneco",
            "genre": "HipHop",
            "id": 1,
            "score": 1
        }
        track2 = {
            "artist": "Stomy Bugsy",
            "genre": "HipHop",
            "id": 2,
            "score": 0.9
        }
        track3 = {
            "artist": "Passi",
            "genre": "HipHop",
            "id": 3,
            "score": 0.8
        }
        track4 = {
            "artist": "Kalash",
            "genre": "HipHop",
            "id": 4,
            "score": 0.1
        }
        self.user1 = User(1, [track1, track2, track1])
        self.user2 = User(2, [track2, track3, track4])

    def test_get_cooccurrence_artist(self):
        expected_result = {
            ('Passi', 'Stomy Bugsy'): 1,
            ('Doc Gyneco', 'Stomy Bugsy'): 2,
            ('Doc Gyneco', 'Doc Gyneco'): 1,
            }
        results = get_cooccurrence([self.user1, self.user2], "artist", 0.8)
        self.assertEqual(results, expected_result)

    def test_get_cooccurrence_id(self):
        expected_result = {
            (2, 3): 1,
            (1, 2): 2,
            (1, 1): 1,
            }
        results = get_cooccurrence([self.user1, self.user2], "id", 0.8)
        self.assertEqual(results, expected_result)

    def test_get_scores_artist(self):
        expected_result = {
            'Kalash': [0.1],
            'Passi': [0.8],
            'Doc Gyneco': [1, 1],
            'Stomy Bugsy': [0.9, 0.9]
        } 
        results = get_scores([self.user1, self.user2], "artist")
        self.assertEqual(results, expected_result)

    def test_get_scores_id(self):
        expected_result = {
            4: [0.1],
            3: [0.8],
            1: [1, 1],
            2: [0.9, 0.9]
        } 
        results = get_scores([self.user1, self.user2], "id")
        self.assertEqual(results, expected_result)

    def test_get_mean_popularity(self):
        expected_result = [
            ('Doc Gyneco', 1.0),
            ('Stomy Bugsy', 0.9),
            ('Passi', 0.8),
            ('Kalash', 0.1)]
        results = get_mean_popularity([self.user1, self.user2], "artist")
        self.assertEqual(results, expected_result)

    def test_get_distinct(self):
        expected_result = 4
        results = get_distinct([self.user1, self.user2], "artist")
        self.assertEqual(results, expected_result)

    def test_get_counts(self):
        expected_result = {
            'Doc Gyneco': 2,
            'Passi': 1,
            'Stomy Bugsy': 2,
            'Kalash': 1,
        }
        results = get_counts([self.user1, self.user2], "artist")
        self.assertEqual(dict(results), expected_result)