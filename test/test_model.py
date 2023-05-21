import unittest

from simulation.model import CommunicationNetwork


class ModelTest(unittest.TestCase):

    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_vertices(self):
        self.assertEqual(len(ModelTest.cn.vertices()), 4)
        self.assertEqual(ModelTest.cn.vertices('h1'), {'v1', 'v2'})

    def test_hyperedges(self):
        self.assertEqual(len(ModelTest.cn.hyperedges()), 3)
        self.assertEqual(ModelTest.cn.hyperedges('v1'), {'h1'})

class ModelTest2(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v1'], 'h2': ['v2', 'v3','v4','v5','v6'], 'h3': ['v1', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_vertices(self):
        self.assertEqual(len(ModelTest2.cn.vertices()), 6)
        self.assertEqual(ModelTest2.cn.vertices('h1'),{'v1','v1'})
        self.assertEqual(ModelTest2.cn.vertices('h1'),{'v1'})
        self.assertEqual(ModelTest2.cn.vertices('h2'),{'v2', 'v3','v4','v5','v6'})

class ModelDataTest(unittest.TestCase):
    def test_model_with_data(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
        self.assertEqual(len(communciation_network.participants()), 37103)
        self.assertEqual(len(communciation_network.channels()), 309740)

        self.assertEqual(len(communciation_network.vertices()), 37103)
        self.assertEqual(len(communciation_network.hyperedges()), 309740)

        self.assertEqual(len(communciation_network.participants()), len(communciation_network.vertices()))

class ModelDataTest2(unittest.TestCase):
    def test_model_with_data(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/testDataNetworks.json')
        self.assertEqual(len(communciation_network.participants()), 4)