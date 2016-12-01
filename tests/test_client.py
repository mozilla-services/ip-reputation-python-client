# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA
import mock

from ipreputation.client import IPReputationClient

TEST_IP = '192.168.0.1'


class IPReputationClientTest(unittest.TestCase):

    def setUp(self):
        self.client = IPReputationClient(
            hawk_id='root',
            hawk_key='toor',
            host='localhost',
            port=8080,
            timeout=3)

    def test_get_ip(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.get(TEST_IP)
            requests.get.assert_called_with(
                'http://localhost:8080/' + TEST_IP,
                auth=self.client.auth)

    def test_add_ip(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.add(TEST_IP, 20)
            requests.post.assert_called_with(
                'http://localhost:8080/',
                auth=self.client.auth,
                json={'ip': TEST_IP, 'reputation': 20})

    def test_update_ip(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.update(TEST_IP, 70)
            requests.put.assert_called_with(
                'http://localhost:8080/' + TEST_IP,
                auth=self.client.auth,
                json={'ip': TEST_IP, 'reputation': 70})

    def test_remove_ip(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.remove(TEST_IP)
            requests.delete.assert_called_with(
                'http://localhost:8080/' + TEST_IP,
                auth=self.client.auth)

    def test_send_violation(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.send_violation(
                TEST_IP, 'test-violation')
            requests.put.assert_called_with(
                'http://localhost:8080/violations/',
                auth=self.client.auth,
                json={'violation': 'test-violation', 'ip': TEST_IP})


if __name__ == '__main__':
    # run python -m tests/test_client.py
    # Test against running service
    print('main')
