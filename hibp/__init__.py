import logging
import datetime
import os.path
from os import mkdir
from hibp.remote import Remote
from hibp.account_list import AccountList
from hibp.mail import Mail


def main():
    logging.basicConfig(filename='log/hibp.log', level=logging.INFO)
    logging.info('Started run at {0}'.format(datetime.datetime.now().isoformat()))
    # Only send an e-mail the first time (or only once?)
    # Use status/account_name/breach.sent
    # List all accounts
    account_list = AccountList().account_list
    # Check for breaches
    account_breached = Remote(account_list).account_breaches
    # Loop. If status/account/breach_name.sent does not exist, send a warning e-mail and create the file
    for account, breaches in account_breached.items():
        if not os.path.exists(os.path.join('status', account)):
            mkdir(os.path.join('status', account))
        # List of breaches the user doesn't know about yet
        uninformed = []
        for breach in breaches:
            if not os.path.exists(os.path.join('status', account, '{0}.sent'.format(breach['Domain']))):
                # This user is in a breach, but doesn't know it yet
                uninformed.append(breach)
                with open(os.path.join('status', account, '{0}.sent'.format(breach['Domain'])), 'w') as f:
                    f.write(datetime.datetime.now().isoformat())
        if len(uninformed) > 0:
            # We need to inform the user
            m = Mail()
            m.send(recipient=account, msg_text=m.breach_msg(account, uninformed))
            logging.info('Send a breach message to {0}'.format(account))
    logging.info('Ended run at {0}'.format(datetime.datetime.now().isoformat()))
