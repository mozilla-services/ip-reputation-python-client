# -*- coding: utf-8 -*-
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # NOQA
import mock
from requests.exceptions import Timeout

from ipreputation.client import IPReputationClient

TEST_IP = '192.168.0.1'
TEST_TIMEOUT = 3 # seconds

class IPReputationClientTest(unittest.TestCase):

    def setUp(self):
        self.client = IPReputationClient(
            hawk_id='root',
            hawk_key='toor',
            host='localhost',
            port=8080,
            timeout=TEST_TIMEOUT)

    def test_get_ip(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.get(TEST_IP)
            requests.get.assert_called_with(
                'http://localhost:8080/' + TEST_IP,
                auth=self.client.auth,
                timeout=TEST_TIMEOUT)

    def test_add_ip(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.add(TEST_IP, 20)
            requests.post.assert_called_with(
                'http://localhost:8080/',
                auth=self.client.auth,
                json={'ip': TEST_IP, 'reputation': 20},
                timeout=TEST_TIMEOUT)

    def test_update_ip(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.update(TEST_IP, 70)
            requests.put.assert_called_with(
                'http://localhost:8080/' + TEST_IP,
                auth=self.client.auth,
                json={'ip': TEST_IP, 'reputation': 70},
                timeout=TEST_TIMEOUT)

    def test_remove_ip(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.remove(TEST_IP)
            requests.delete.assert_called_with(
                'http://localhost:8080/' + TEST_IP,
                auth=self.client.auth,
                timeout=TEST_TIMEOUT)

    def test_send_violation(self):
        with mock.patch('ipreputation.client.requests') as requests:
            self.client.send_violation(
                TEST_IP, 'test-violation')
            requests.put.assert_called_with(
                'http://localhost:8080/violations/',
                auth=self.client.auth,
                json={'violation': 'test-violation', 'ip': TEST_IP},
                timeout=TEST_TIMEOUT)



def integration_test():
    """
    Tests against running tigerblood service.

    run with: make tests-integration
    """
    client = IPReputationClient(
        hawk_id='root',
        hawk_key='toor',
        host='localhost',
        port=8080,
        timeout=3)

    # clear entry for our TEST_IP
    response = client.remove(TEST_IP)

    # does not get reputation for a nonexistent IP
    response = client.get(TEST_IP)
    assert response.status_code == 404, "Cannot get TEST IP: {}.".format(TEST_IP)

    # does not update reputation for nonexistent IP
    response = client.update(TEST_IP, 500)
    assert response.status_code == 404, "Cannot update TEST IP: {}".format(TEST_IP)

    # does not remove reputation for a nonexistent IP
    response = client.remove(TEST_IP)
    assert response.status_code == 200, "Cannot remove TEST IP: {}".format(TEST_IP)

    # adds reputation for new IP
    response = client.add(TEST_IP, 50)
    assert response.status_code == 201

    # does not add reputation for existing IP
    response = client.add(TEST_IP, 50)
    assert response.status_code == 409

    # updates reputation for existing IP
    response = client.update(TEST_IP, 5)
    assert response.status_code == 200

    # removes reputation for existing IP
    response = client.remove(TEST_IP)
    assert response.status_code == 200

    # sends a violation
    response = client.send_violation(TEST_IP, 'test_violation')
    assert response.status_code == 204

    # times out a GET request
    timeout_client = IPReputationClient(
        hawk_id='root',
        hawk_key='toor',
        host='localhost',
        port=8080,
        timeout=0.0001) # 0.1 ms

    timed_out = False
    try:
        timeout_client.get(TEST_IP)
    except Timeout:
        timed_out = True
    assert timed_out == True


if __name__ == '__main__':
    integration_test()
