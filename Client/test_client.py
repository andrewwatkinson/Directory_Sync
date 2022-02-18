import unittest
import client
from unittest.mock import patch
from os import getcwd, remove
from os.path import getsize
import pickle


class TestClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.current_directory = (getcwd())

    def setUp(self) -> None:
        self.cl1 = client.Client(5001, "localhost", self.current_directory)

    def test_hash_file(self):
        with open("hash_test.txt", 'wt') as file:
            file.write("this is a test")
            file.close()
        self.assertEqual(client.hash_file("hash_test.txt"), "2e99758548972a8e8822ad47fa1017ff72f06f3ff6a016851f45c398732bc50c")
        remove("hash_test.txt")

    def test_segment_hashes(self):
        file_name = "hash_test.txt"
        with open(file_name, 'wt') as file:
            file.write("this is a test")
            file.close()
        ground_truth = ['42b57632c93fb87d5f6de87d299eeda64dadbb61376eb196bce5c58cefaac594', '72b9fe19acb934aff521f1f46b2ddd7ef821df42ea523f674c270314322133b3']
        self.assertEqual(client.segment_hashes(file_name, getsize(file_name)//2), ground_truth)
        remove("hash_test.txt")

    def test_send_variable(self):
        with patch('client.socket.socket') as mocked_socket:
            self.cl1.s = mocked_socket
            self.cl1.send_variable(["test", "test"])

    def test_flag_partial_check(self):
        with open("test_seg.txt", 'wt') as file:
            file.write("this is a test")
            file.close()

        with patch('client.socket.socket') as mocked_socket:
            mocked_socket.return_value.recv.return_value = pickle.dumps([])
            self.cl1.s = mocked_socket
            self.cl1.sense = 2
            self.cl1.flag_partial(["test_seg.txt"])


