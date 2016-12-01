from requests_hawk import HawkAuth
import requests


class IPReputationClient(object):
    "Client for the Tigerblood IP Reputation Service."

    def __init__(self, hawk_id, hawk_key, host, port=80, timeout=30):
        self.base_url = 'http://{}:{}/'.format(host, port)
        self.auth = HawkAuth(id=hawk_id, key=hawk_key)

    def get(self, ip):
        return requests.get(self.base_url + ip, auth=self.auth)

    def add(self, ip, reputation):
        return requests.post(
            self.base_url,
            auth=self.auth,
            json={'ip': ip, 'reputation': reputation})

    def update(self, ip, reputation):
        return requests.put(self.base_url + ip,
                            auth=self.auth,
                            json={'ip': ip, 'reputation': reputation})

    def remove(self, ip):
        return requests.delete(self.base_url + ip, auth=self.auth)

    def send_violation(self, ip, violation_type):
        return requests.put(self.base_url + 'violations/',
                            auth=self.auth,
                            json={'ip': ip, 'violation': violation_type})
