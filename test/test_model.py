import unittest
import bz2
from unittest import mock

from datetime import datetime

from simulation.model import CommunicationNetwork
from simulation.model import EntityNotFound

class ModelTest(unittest.TestCase):

    cn = CommunicationNetwork({'h1': ['v1', 'v2'], 'h2': ['v2', 'v3'], 'h3': ['v3', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_vertices(self):
        self.assertEqual(len(ModelTest.cn.vertices()), 4)
        self.assertEqual(ModelTest.cn.vertices('h1'), {'v1', 'v2'})

    def test_hyperedges(self):
        self.assertEqual(len(ModelTest.cn.hyperedges()), 3)
        self.assertEqual(ModelTest.cn.hyperedges('v1'), {'h1'})

class ModelTestBasics(unittest.TestCase):
    cn = CommunicationNetwork({'h1': ['v1', 'v1'], 'h2': ['v2', 'v3','v4','v5','v6'], 'h3': ['v1', 'v4']}, {'h1': 1, 'h2': 2, 'h3': 3})

    def test_vertices(self):
        self.assertEqual(len(ModelTestBasics.cn.vertices()), 6)
        self.assertEqual(ModelTestBasics.cn.vertices(),{'v1','v2', 'v3','v4','v5','v6'})
        self.assertEqual(ModelTestBasics.cn.vertices(),{'v1','v1','v2', 'v3','v4','v5','v6'})
        self.assertEqual(ModelTestBasics.cn.vertices('h1'),{'v1','v1'})
        self.assertEqual(ModelTestBasics.cn.vertices('h1'),{'v1'})
        self.assertEqual(ModelTestBasics.cn.vertices('h2'),{'v2', 'v3','v4','v5','v6'})
    
    def test_vertices_unknown_hedge(self):
        with self.assertRaises(EntityNotFound):
            ModelTestBasics.cn.vertices('Unknown_hedge')

    def test_vertices_equal_participants(self):
        self.assertEqual(len(ModelTestBasics.cn.vertices()),len(ModelTestBasics.cn.participants()))
        self.assertEqual(ModelTestBasics.cn.vertices(),ModelTestBasics.cn.participants())

    
    def test_hyperedges(self):
        self.assertEqual(len(ModelTestBasics.cn.hyperedges()), 3)
        self.assertEqual(ModelTestBasics.cn.hyperedges('v1'),{'h1','h3'})
        self.assertEqual(ModelTestBasics.cn.hyperedges('v2'),{'h2'})

    def test_hyperedges_unknown_vertic(self):
        with self.assertRaises(EntityNotFound):
            ModelTestBasics.cn.hyperedges('Unknown_vertic')

    def test_hyperedges_equal_channels(self):
        self.assertEqual(len(ModelTestBasics.cn.hyperedges()),len(ModelTestBasics.cn.channels()))
        self.assertEqual(ModelTestBasics.cn.hyperedges(),ModelTestBasics.cn.channels())


    def test_timings(self):
        self.assertEqual(ModelTestBasics.cn.timings(),{'h1': 1, 'h2': 2, 'h3': 3})
        self.assertEqual(ModelTestBasics.cn.timings('h1'), 1)

    def test_timings_unknown_hedge(self):
        with self.assertRaises(KeyError):
            ModelTestBasics.cn.timings('Unknown_hedge')


class ModelTestBadContent(unittest.TestCase):
    
    def test_verifie_data_validation_of_vertice_with_stringItem(self):
        with self.assertRaises(Exception):
            CommunicationNetwork({'h1': 'v1'}, { 'h1': 1})

    def test_verifie_data_validation_of_vertice_with_empty_dictItem(self):
        with self.assertRaises(Exception):
            CommunicationNetwork({'h1': {}}, { 'h1': 1})
    
    def test_verifie_data_validation_of_vertice_with_no_item(self):
        with self.assertRaises(AttributeError):
            CommunicationNetwork({'h1'}, { 'h1': 1})
    
    def test_verifie_data_validation_of_vertice_with_empty_dict(self):
        with self.assertRaises(Exception):
            CommunicationNetwork({}, { 'h1': 1})
    
    def test_verifie_data_validation_of_empty_timings(self):
        with self.assertRaises(Exception):
            CommunicationNetwork({'h1':['v1']},{})

    def test_verifie_data_validation_of_extra_timings(self):
        with self.assertRaises(Exception):
            CommunicationNetwork({'h1':['v1']},{'h1': 1, 'h2': 2})

    def test_verifie_data_validation_of_double_hedge(self):
            cn = CommunicationNetwork({'h1': ['v1'], 'h1': ['v2']}, { 'h1': 1})
            self.assertEqual(cn.vertices('h1'),{'v2'})

class ModelParsFromJson(unittest.TestCase):
    def test_from_json(self):
        fakeResponse = '{"Review_1":{"bound": "bounded", "end":"2023-05-26T12:01:01", "participants": ["Anton","Simon"], "start":"2023-05-26T09:01:01"}}'
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fakeResponse):
            result = CommunicationNetwork.from_json("fakePath.json", name= "mockedOpen")
            self.assertEqual(result.participants('Review_1'),{'Anton','Simon'})
            self.assertEqual(result.timings('Review_1'), datetime.fromisoformat("2023-05-26T12:01:01"))
            self.assertEqual(result.name,'mockedOpen')

    def test_from_json_missing_non_importent(self):
        fakeResponse = '{"Review_1":{ "end":"2023-05-26T12:01:01", "participants": ["Anton","Simon"]}}'
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fakeResponse):
            result = CommunicationNetwork.from_json("fakePath.json", name= "mockedOpen")
            self.assertEqual(result.participants('Review_1'),{'Anton','Simon'})
            self.assertEqual(result.timings('Review_1'), datetime.fromisoformat("2023-05-26T12:01:01"))
            self.assertEqual(result.name,'mockedOpen')
    
    def test_from_json_missing_end(self):
        fakeResponse = '{"Review_1":{"bound": "bounded", "participants": ["Anton","Simon"], "start":"2023-05-26T09:01:01"}}'
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fakeResponse):
            with self.assertRaises(KeyError):
                CommunicationNetwork.from_json("fakePath.json", name= "mockedOpen")
    
    def test_from_json_missing_participants(self):
        fakeResponse = '{"Review_1":{ "end":"2023-05-26T12:01:01"}}'
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fakeResponse):
            with self.assertRaises(KeyError):
                CommunicationNetwork.from_json("fakePath.json", name= "mockedOpen")

    def test_from_json_missing_channel(self):
        fakeResponse = '{"end":"2023-05-26T12:01:01", "participants": ["Anton","Simon"]}'
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fakeResponse):
            with self.assertRaises(Exception):
                CommunicationNetwork.from_json("fakePath.json", name= "mockedOpen")

    def test_from_json_not_isoformat(self):
        fakeResponse = '{"Review_1":{ "end":"2023/05/26 12:01:01", "participants": ["Anton","Simon"]}}'
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fakeResponse):
            with self.assertRaises(ValueError):
                CommunicationNetwork.from_json("fakePath.json", name= "mockedOpen")

    def test_from_json_double_end(self):
        fakeResponse = '{"Review_1":{ "end":"2023-05-26T12:01:01","end":"2023-05-26T09:01:01", "participants": ["Anton","Simon"]}}'
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fakeResponse):
            with self.assertRaises(Exception):
                CommunicationNetwork.from_json("fakePath.json", name= "mockedOpen")


class ModelParsFromJsonBz2(unittest.TestCase):
    def test_from_json_bz2(self):
        fakeResponse = bz2.compress(b'{"Review_1":{"bound": "bounded", "end":"2023-05-26T12:01:01", "participants": ["Anton","Simon"], "start":"2023-05-26T09:01:01"}}')
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fakeResponse):
            result = CommunicationNetwork.from_json("fakePath.json.bz2", name= "mockedOpen")
            self.assertEqual(result.participants('Review_1'),{'Anton','Simon'})
            self.assertEqual(result.timings('Review_1'), datetime.fromisoformat("2023-05-26T12:01:01"))
            self.assertEqual(result.name,'mockedOpen')

    def test_from_json_wrong_compress(self):
        fakeResponse = b'{"Review_1":{"bound": "bounded", "end":"2023-05-26T12:01:01", "participants": ["Anton","Simon"], "start":"2023-05-26T09:01:01"}}'
        with mock.patch('simulation.model.Path.open', new_callable=mock.mock_open, read_data = fakeResponse):
            with self.assertRaises(Exception):
                CommunicationNetwork.from_json("fakePath.json.bz2", name= "mockedOpen")          

class ModelDataTest(unittest.TestCase):
    def test_model_with_data(self):
        communciation_network = CommunicationNetwork.from_json('./data/networks/microsoft.json.bz2')
        self.assertEqual(len(communciation_network.participants()), 37103)
        self.assertEqual(len(communciation_network.channels()), 309740)

        self.assertEqual(len(communciation_network.vertices()), 37103)
        self.assertEqual(len(communciation_network.hyperedges()), 309740)

        self.assertEqual(len(communciation_network.participants()), len(communciation_network.vertices()))
