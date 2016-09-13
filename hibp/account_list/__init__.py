from os import listdir
from os.path import isfile, join


class AccountList:
    def __init__(self):
        self.account_dir = 'accounts'
        # List of all the files in accounts; contains all the accounts to check
        account_files = [f for f in listdir(self.account_dir) if isfile(join(self.account_dir, f))]
        self.account_list = self.enumerate(account_files)

    def enumerate(self, account_files):
        accounts = []
        for account_file in account_files:
            with open(join(self.account_dir, account_file), 'r') as f:
                accounts += f.readlines()
        return accounts
