import unittest
import bz2
from unittest import mock
from datetime import datetime
from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType


class MinimalPath(unittest.TestCase):
    communication_network = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_1(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.communication_network, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_2(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.communication_network, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.communication_network, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_3(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.communication_network, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.communication_network, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_4(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.communication_network, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.communication_network, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_same_timings(self):
        communication_network = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 1, 'h3': 1})
        with self.assertRaises(Exception):
            self.assertEqual(single_source_dijkstra_vertices(communication_network, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2':1})
        #single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)

class MinimalPathExceptionHandeling(unittest.TestCase):

    def test_minimal_path_unknown_vertice(self):
        communication_network = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(communication_network, 'v5', DistanceType.SHORTEST, min_timing=0)

        with self.assertRaises(Exception):
            single_source_dijkstra_hyperedges(communication_network, 'v5', DistanceType.SHORTEST, min_timing=0)


    def test_minimal_path_unknown_distance_type(self):
        communication_network = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

        with self.assertRaises(UnboundLocalError):
            single_source_dijkstra_vertices(communication_network, 'v1', DistanceType, min_timing=0)

        with self.assertRaises(UnboundLocalError):
            single_source_dijkstra_hyperedges(communication_network, 'v1', DistanceType, min_timing=0)

class TestWeirdTimings(unittest.TestCase):
    communication_network = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})
    def letter_vertice(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(TestWeirdTimings.communication_network, 'v1', DistanceType.SHORTEST, min_timing='a')
    def letter_hyperedges(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_hyperedges(TestWeirdTimings.communication_network, 'v1', DistanceType.SHORTEST, min_timing='e')
    def list_verice(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(TestWeirdTimings.communication_network, 'v1', DistanceType.SHORTEST, min_timing=[])
    def list_hyperedge(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(TestWeirdTimings.communication_network, 'v1', DistanceType.SHORTEST, min_timing={})
    def float_vertice(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(TestWeirdTimings.communication_network, 'v1', DistanceType.FASTEST, min_timing=0.2353535)
    def float_hyperedge(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_hyperedges(TestWeirdTimings.communication_network, 'v2', DistanceType.FASTEST, min_timing=0.2325253262)
    def float_fore_vertice(self):
        single_source_dijkstra_vertices(TestWeirdTimings.communication_network, 'v1', DistanceType.FOREMOST, min_timing=0.2353535)
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(TestWeirdTimings.communication_network, 'v1', DistanceType.FOREMOST, min_timing=0.2353535)

class TestOwnFile(unittest.TestCase):
    communication_network = CommunicationNetwork.from_json('./data/networks/SimpleTestData.json')

    def test_shortest(self):
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 1, DistanceType.SHORTEST, min_timing=0), {2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:2, 9:2, 10:2})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 2, DistanceType.SHORTEST, min_timing=0), {1:1, 3:1, 4:1, 5:2, 6:2, 7:2, 8:2, 9:1, 10:1})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 3, DistanceType.SHORTEST, min_timing=0), {1:1, 2:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:2, 10:2})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 4, DistanceType.SHORTEST, min_timing=0), {1:1, 2:1, 3:1, 5:2, 6:2, 7:1, 8:2, 9:2, 10:2})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 5, DistanceType.SHORTEST, min_timing=0), {1:1, 2:3, 3:1, 4:2, 6:1, 7:1, 8:2, 9:4, 10:4})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 6, DistanceType.SHORTEST, min_timing=0), {1:1, 2:2, 3:1, 4:2, 5:1, 7:1, 8:1, 9:3, 10:3})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 7, DistanceType.SHORTEST, min_timing=0), {1:1, 2:2, 3:1, 4:1, 5:1, 6:1, 8:1, 9:3, 10:3})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 8, DistanceType.SHORTEST, min_timing=0), {1:2, 2:2, 3:1, 4:2, 5:2, 6:1, 7:1, 9:3, 10:3})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 9, DistanceType.SHORTEST, min_timing=0), {2:1, 10:1})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 10, DistanceType.SHORTEST, min_timing=0), {2:1, 9:1})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.communication_network, 11, DistanceType.SHORTEST, min_timing=0), {})

        #hyperedges

        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 1, DistanceType.SHORTEST, min_timing=0), {2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:2, 9:2, 10:2})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 2, DistanceType.SHORTEST, min_timing=0), {1:1, 3:1, 4:1, 5:2, 6:2, 7:2, 8:2, 9:1, 10:1})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 3, DistanceType.SHORTEST, min_timing=0), {1:1, 2:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:2, 10:2})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 4, DistanceType.SHORTEST, min_timing=0), {1:1, 2:1, 3:1, 5:2, 6:2, 7:1, 8:2, 9:2, 10:2})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 5, DistanceType.SHORTEST, min_timing=0), {1:1, 2:3, 3:1, 4:2, 6:1, 7:1, 8:2, 9:4, 10:4})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 6, DistanceType.SHORTEST, min_timing=0), {1:1, 2:2, 3:1, 4:2, 5:1, 7:1, 8:1, 9:3, 10:3})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 7, DistanceType.SHORTEST, min_timing=0), {1:1, 2:2, 3:1, 4:1, 5:1, 6:1, 8:1, 9:3, 10:3})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 8, DistanceType.SHORTEST, min_timing=0), {1:2, 2:2, 3:1, 4:2, 5:2, 6:1, 7:1, 9:3, 10:3})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 9, DistanceType.SHORTEST, min_timing=0), {2:1, 10:1})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 10, DistanceType.SHORTEST, min_timing=0), {2:1, 9:1})
        self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.communication_network, 11, DistanceType.SHORTEST, min_timing=0), {})


    # def test2(self):
    #     cn2 = CommunicationNetwork({'h1': ["Axel", "Simon"], 'h2' : ["Donald"]}, {'h1':1, 'h2':2})
    #     self.assertEqual(single_source_dijkstra_vertices(cn2, "Axel", DistanceType.SHORTEST, min_timing=3), {"Simon":1})
    #     self.assertEqual(single_source_dijkstra_vertices(cn2, "Donald", DistanceType.SHORTEST, min_timing=0), {})

class TestingFastestAndForemost(unittest.TestCase):
    communication_network = CommunicationNetwork({'h1' : ["Axel", "Simon"], 'h2' : ["Donald", "Simon", "Anton"], 'h3' : ["Axel", "Daniel", "Joakim", "Harald"], 'h4': ["Anton"]}, {'h1':1, 'h2':2, 'h3':3, 'h4':4})

    def test_fastest(self):
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Axel", DistanceType.FASTEST, min_timing=0), {"Simon":0, "Anton":1,"Donald":1,"Joakim":0,"Daniel":0,"Harald":0})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Simon", DistanceType.FASTEST, min_timing=0), {"Axel":0, "Anton":0, "Donald": 0, "Joakim":2,"Daniel":2,"Harald":2})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Anton", DistanceType.FASTEST, min_timing=0), {"Simon":0, "Donald":0})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Joakim", DistanceType.FASTEST, min_timing=0), {"Axel":0, "Harald":0, "Daniel": 0})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Donald", DistanceType.FASTEST, min_timing=0), {"Simon":0, "Anton":0})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Harald", DistanceType.FASTEST, min_timing=0), {"Axel":0, "Joakim":0, "Daniel": 0})

        #Hyperedges

        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Axel", DistanceType.FASTEST, min_timing=0), {"Simon":0, "Anton":1,"Donald":1,"Joakim":0,"Daniel":0,"Harald":0})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Simon", DistanceType.FASTEST, min_timing=0), {"Axel":0, "Anton":0, "Donald": 0, "Joakim":2,"Daniel":2,"Harald":2})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Anton", DistanceType.FASTEST, min_timing=0), {"Simon":0, "Donald":0})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Joakim", DistanceType.FASTEST, min_timing=0), {"Axel":0, "Harald":0, "Daniel": 0})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Donald", DistanceType.FASTEST, min_timing=0), {"Simon":0, "Anton":0})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Harald", DistanceType.FASTEST, min_timing=0), {"Axel":0, "Joakim":0, "Daniel": 0})

    def test_foremost(self):

        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Axel", DistanceType.FOREMOST, min_timing=0), {"Simon":1, "Anton":2,"Donald":2,"Joakim":3,"Daniel":3,"Harald":3})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Simon", DistanceType.FOREMOST, min_timing=0), {"Axel":1, "Anton":2, "Donald": 2, "Joakim":3,"Daniel":3,"Harald":3})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Anton", DistanceType.FOREMOST, min_timing=0), {"Simon":2, "Donald":2})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Joakim", DistanceType.FOREMOST, min_timing=0), {"Axel":3, "Harald":3, "Daniel": 3})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Donald", DistanceType.FOREMOST, min_timing=0), {"Simon":2, "Anton":2})
        self.assertEqual(single_source_dijkstra_vertices(TestingFastestAndForemost.communication_network, "Harald", DistanceType.FOREMOST, min_timing=0), {"Axel":3, "Joakim":3, "Daniel": 3})

        #Hyperedges

        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Axel", DistanceType.FOREMOST, min_timing=0), {"Simon":1, "Anton":2,"Donald":2,"Joakim":3,"Daniel":3,"Harald":3})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Simon", DistanceType.FOREMOST, min_timing=0), {"Axel":1, "Anton":2, "Donald": 2, "Joakim":3,"Daniel":3,"Harald":3})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Anton", DistanceType.FOREMOST, min_timing=0), {"Simon":2, "Donald":2})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Joakim", DistanceType.FOREMOST, min_timing=0), {"Axel":3, "Harald":3, "Daniel": 3})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Donald", DistanceType.FOREMOST, min_timing=0), {"Simon":2, "Anton":2})
        self.assertEqual(single_source_dijkstra_hyperedges(TestingFastestAndForemost.communication_network, "Harald", DistanceType.FOREMOST, min_timing=0), {"Axel":3, "Joakim":3, "Daniel": 3})


class TestingWithBz2(unittest.TestCase):
    def test_from_json_bz2(self):
        fake_response = bz2.compress(b'{"Review_1":{"bound": "bounded", "end":"2023-05-26T12:01:01", "participants": ["Anton","Simon"], "start":"2023-05-26T09:01:01"}}')
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fake_response):
            communication_network = CommunicationNetwork.from_json("fakePath.json.bz2", name= "mockedOpen")
            single_source_dijkstra_vertices(communication_network, "Anton", DistanceType.SHORTEST, min_timing=0)
            single_source_dijkstra_hyperedges(communication_network, "Anton", DistanceType.SHORTEST, min_timing=0)
            with self.assertRaises(Exception):
                communication_network = CommunicationNetwork.from_json("fakePath.json.bz2", name= "mockedOpen")
                single_source_dijkstra_vertices(communication_network, "Anton", DistanceType.FASTEST, min_timing=0)
            with self.assertRaises(Exception):
                communication_network = CommunicationNetwork.from_json("fakePath.json.bz2", name= "mockedOpen")
                single_source_dijkstra_hyperedges(communication_network, "Anton", DistanceType.FASTEST, min_timing=0)
            with self.assertRaises(Exception):
                communication_network = CommunicationNetwork.from_json("fakePat.json.bz2", name= "mockedOpen")
                single_source_dijkstra_vertices(communication_network, "Anton", DistanceType.FOREMOST, min_timing=0)
            with self.assertRaises(Exception):
                communication_network = CommunicationNetwork.from_json("fakePath.json.bz2", name= "mockedOpen")
                single_source_dijkstra_hyperedges(communication_network, "Anton", DistanceType.FOREMOST, min_timing=0)

class BadData(unittest.TestCase):
    communication_network = CommunicationNetwork.from_json('./data/networks/SimpleTestData.json')
    def test_fastest(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(BadData.communication_network, 1, DistanceType.FASTEST, min_timing=0)

    def test_foremost(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(BadData.communication_network, 1, DistanceType.FOREMOST, min_timing=0)

    def test_invalid_vertice(self):
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(BadData.communication_network, 0, DistanceType.FOREMOST, min_timing=0)
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(BadData.communication_network, 0, DistanceType.FASTEST, min_timing=0)
        with self.assertRaises(Exception):
            single_source_dijkstra_vertices(BadData.communication_network, 0, DistanceType.SHORTEST, min_timing=0)

    def test_invalid_vertice_to_find(self):
        with self.assertRaises(Exception):
            self.assertEqual(single_source_dijkstra_vertices(BadData.communication_network, 1, DistanceType.FOREMOST, min_timing=0), {12:1})
        with self.assertRaises(Exception):
            self.assertEqual(single_source_dijkstra_vertices(BadData.communication_network, 1, DistanceType.FASTEST, min_timing=0), {12:1})
        with self.assertRaises(Exception):
            self.assertEqual(single_source_dijkstra_vertices(BadData.communication_network, 1, DistanceType.SHORTEST, min_timing=0), {12:1})

    # def test_invalid_hyperedge(self):
    #     with self.assertRaises(Exception):
    #         self.assertEqual(single_source_dijkstra_hyperedges(BadData.cn, 1, DistanceType.FOREMOST, min_timing=0), {12:1})

    #     with self.assertRaises(Exception):
    #         self.assertEqual(single_source_dijkstra_hyperedges(BadData.cn, "a", DistanceType.FOREMOST, min_timing=0), {2: 12})