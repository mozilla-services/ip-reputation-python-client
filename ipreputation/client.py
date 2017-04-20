from requests_hawk import HawkAuth
import requests


class IPReputationClient(object):
    "Client for the Tigerblood IP Reputation Service."

    # timeout is in seconds
    # http://docs.python-requests.org/en/master/user/quickstart/#timeouts
    def __init__(self, hawk_id, hawk_key, host, port=80, timeout=30):
        self.base_url = 'http://{}:{}/'.format(host, port)
        self.auth = HawkAuth(id=hawk_id, key=hawk_key)
        self.timeout = timeout

    def get(self, ip):
        return requests.get(self.base_url + ip, auth=self.auth, timeout=self.timeout)

    def add(self, ip, reputation):
        return requests.post(
            self.base_url,
            auth=self.auth,
            json={'ip': ip, 'reputation': reputation},
            timeout=self.timeout)

    def update(self, ip, reputation):
        return requests.put(self.base_url + ip,
                            auth=self.auth,
                            json={'ip': ip, 'reputation': reputation},
                            timeout=self.timeout)

    def remove(self, ip):
        return requests.delete(self.base_url + ip,
                               auth=self.auth,
                               timeout=self.timeout)

    def send_violation(self, ip, violation_type):
        return requests.put(self.base_url + 'violations/' + ip,
                            auth=self.auth,
                            json={'ip': ip, 'violation': violation_type},
                            timeout=self.timeout)
