import requests
import logging
from time import sleep


class Remote:

    def __init__(self, account_list):
        self.account_breaches = {}
        for account in account_list:
            self.account_breaches[account.rstrip()] = self.check(account.rstrip())

    def check(self, account):
        sleep(3)
        r = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/{0}'.format(account),
                         headers=self.headers())
        if r.status_code == 200:
            # The account is in a breach (and the breach is always an array)
            logging.info('{0}: IN LEAK'.format(account))
            return r.json()
        elif r.status_code == 404:
            # The account is not in a breach
            logging.info('{0}: SAFE'.format(account))
            return []
        elif r.status_code == 429:
            # We were too fast and have been throttled
            sleep(3)
            return self.check(account)
        else:
            # Now this is strange
            logging.error('{0}: {1}'.format(account, r.status_code))
            return []

    def headers(self):
        return {
            'user-agent': 'PACKED HIBP Checker/v1.0'
        }
