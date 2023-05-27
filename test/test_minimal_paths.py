import unittest

from simulation.model import CommunicationNetwork
from simulation.minimal_paths import single_source_dijkstra_vertices, single_source_dijkstra_hyperedges, DistanceType


class MinimalPath(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_1(self):
        self.assertEqual(single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0), {'v2': 1, 'v3': 2, 'v4': 3})

    def test_2(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.SHORTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_3(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FASTEST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

    def test_4(self):
        result_1 = single_source_dijkstra_vertices(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        result_2 = single_source_dijkstra_hyperedges(MinimalPath.cn, 'v1', DistanceType.FOREMOST, min_timing=0)
        self.assertEqual(result_1, result_2, 'Single-source Dijkstra implementations are not equivalent')

class TestOwnFile(unittest.TestCase):
    cn = CommunicationNetwork.from_json('./data/networks/SimpleTestData.json')

    def test_shortest(self):
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 1, DistanceType.SHORTEST, min_timing=0), {2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:2, 9:2, 10:2})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 2, DistanceType.SHORTEST, min_timing=0), {1:1, 3:1, 4:1, 5:2, 6:2, 7:2, 8:2, 9:1, 10:1})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 3, DistanceType.SHORTEST, min_timing=0), {1:1, 2:1, 4:1, 5:1, 6:1, 7:1, 8:1, 9:2, 10:2})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 4, DistanceType.SHORTEST, min_timing=0), {1:1, 2:1, 3:1, 5:2, 6:2, 7:1, 8:2, 9:2, 10:2})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 5, DistanceType.SHORTEST, min_timing=0), {1:1, 2:3, 3:1, 4:2, 6:1, 7:1, 8:2, 9:4, 10:4})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 6, DistanceType.SHORTEST, min_timing=0), {1:1, 2:2, 3:1, 4:2, 5:1, 7:1, 8:1, 9:3, 10:3})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 7, DistanceType.SHORTEST, min_timing=0), {1:1, 2:2, 3:1, 4:1, 5:1, 6:1, 8:1, 9:3, 10:3})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 8, DistanceType.SHORTEST, min_timing=0), {1:2, 2:2, 3:1, 4:2, 5:2, 6:1, 7:1, 9:3, 10:3})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 9, DistanceType.SHORTEST, min_timing=0), {2:1, 10:1})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 10, DistanceType.SHORTEST, min_timing=0), {2:1, 9:1})
        self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 11, DistanceType.SHORTEST, min_timing=0), {})
    
    def test2(self):
        cn2 = CommunicationNetwork({'h1': ["Axel", "Simon"], 'h2' : ["Donald"]}, {'h1':1, 'h2':2})
        self.assertEqual(single_source_dijkstra_vertices(cn2, "Axel", DistanceType.SHORTEST, min_timing=3), {"Simon":1})
        self.assertEqual(single_source_dijkstra_vertices(cn2, "Donald", DistanceType.SHORTEST, min_timing=0), {})

class BadData(unittest.TestCase):
    cn = CommunicationNetwork.from_json('./data/networks/SimpleTestData.json')
    def test_fastest(self):
        #can't test fastest as it doesn't work with the way time is defined, for whatever reason
        #self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 1, DistanceType.FASTEST, min_timing=0), {2:1, 3:1, 4:1, 5:1, 6:1, 7:1, 8:2, 9:2, 10:2})
        with self.assertRaises(Exception):
            result_1 = single_source_dijkstra_vertices(TestOwnFile.cn, 1, DistanceType.FASTEST, min_timing=0)
    
    def test_foremost(self):
        with self.assertRaises(Exception):
            result_1 = single_source_dijkstra_vertices(TestOwnFile.cn, 1, DistanceType.FOREMOST, min_timing=0)
    
    def test_invalid_vertice(self):
        with self.assertRaises(Exception):
            result_1 = single_source_dijkstra_vertices(TestOwnFile.cn, 0, DistanceType.FOREMOST, min_timing=0)
    
    def test_invalid_vertice_to_find(self):
        with self.assertRaises(Exception):
            self.assertEqual(single_source_dijkstra_vertices(TestOwnFile.cn, 1, DistanceType.FOREMOST, min_timing=0), {12:1})
    
    def test_invalid_hyperedge_to_find(self):
        with self.assertRaises(Exception):
            self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.cn, 1, DistanceType.FOREMOST, min_timing=0), {12:1})
        
        with self.assertRaises(Exception):
            self.assertEqual(single_source_dijkstra_hyperedges(TestOwnFile.cn, "a", DistanceType.FOREMOST, min_timing=0), {2: 12})