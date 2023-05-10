from Account import Account
from Printer import Printer
import requests
import time
import random


class AccountManager:
    def __init__(self, system_manager):
        self.accounts = []
        self.groups = []
        self.system_manager = system_manager

    def get_accounts(self):
        return self.accounts

    def get_groups(self):
        return self.groups

    def set_accounts(self, accounts):
        self.accounts = accounts

    def set_groups(self, groups):
        self.groups = groups

    def remove_account(self, account):
        self.accounts.remove(account)

    def prepare_accounts(self):
        todel = []

        try:
            for account in self.accounts:
                prepared = account.prepare()

                if not prepared:
                    todel.append(account)

            Printer.print(
                '                                                      ', ending=True)
            Printer.print('[green]All accounts prepared!', timestamp=True)
            Printer.print_line_center()
        except:
            Printer.print_error('LE01', 'Error while preparing accounts!')
            self.system_manager.kill_system(5)

        for account in todel:
            self.remove_account(account)

    def load_accounts(self, group=None):
        self.accounts.clear()
        self.groups.clear()

        if group == None:

            Printer.print_line_center()
            Printer.print(
                '[magenta]Which group of accounts would you like to run? (blank for all)', timestamp=True)
            Printer.print('[magenta]X[white]) Go back', timestamp=True)
            inpt = Printer.input('[white]> ', timestamp=True)

            if inpt.lower() == 'x':
                self.system_manager.get_menu_handler().main_menu(True)
                pass

        else:
            inpt = ""

        Printer.print_line_center()
        Printer.print('[yellow]Reading account data...', timestamp=True, ending=True)

        try:
            todel = []
            raw_accounts = []
            raw_accounts, self.groups = self.system_manager.get_file_manager().read_accounts(inpt)
            counter = 0

            for account in raw_accounts:
                counter += 1
                Printer.print('[yellow]Reading account data.. (' + str(counter) + '/' + str(len(raw_accounts)) + ').', timestamp=True, ending=True)
                if not (account['Proxy'] == None or account['Proxy'] == ''):
                    try:
                        host, port, user, password = account['Proxy'].split(
                            ":")
                    except:
                        Printer.print_error(
                            'FM03', 'One of your proxies is corrupted!')
                        todel.append(account)
                        continue
                    try:
                        write_proxy = account['Proxy']
                        proxy = {
                            'http': 'http://' + f"{user}:{password}@{host}:{port}",
                            'https': 'http://' + f"{user}:{password}@{host}:{port}"
                        }

                        new_account = Account(self.system_manager, group=account['Group'], login=account['Login'],
                                                password=account['Password'], handle=account['Handle'], proxy=proxy, write_proxy=write_proxy)
                        self.accounts.append(new_account)
                    except:
                        Printer.print_error(
                            'FM04', 'One of your proxies is corrupted!')
                        todel.append(account)
                        continue
                else:
                    new_account = Account(
                        self.system_manager, group=account['Group'], login=account['Login'], password=account['Password'], handle=account['Handle'])
                    self.accounts.append(new_account)
                    Printer.print(
                        f'[yellow]No proxy has been inputted for @{new_account.get_handle()}. It will be ran localhost.', timestamp=True)
                if account['Token'] == None or account['Token'] == '':
                    new_account.fetch_token()
                    self.system_manager.get_file_manager().update_account(new_account)
                else:
                    new_account.set_token(account['Token'])
        except Exception as e:
            Printer.print_error("FM02", "Could not read your accounts.csv!")
            self.system_manager.kill_system(5)

        Printer.print(
            '                                                                                                    ', ending=True)
        Printer.print('[green]Account data saved!',
                      timestamp=True, ending=True)
        Printer.print('')

    def follow_other_accounts(self):
        try:
            for tofollow in self.accounts:
                for account in self.accounts:
                    try:
                        if account.get_handle() == tofollow.get_handle():
                            continue

                        account.follow_user_by_screenname(
                            tofollow.get_handle())
                    except:
                        Printer.print(
                            f'[red]Failed to follow an account: {tofollow.get_handle()} - On your Account: {account.get_handle()}', timestamp=True)
                        time.sleep(random.uniform(float(self.system_manager.get_delay(
                        ) - 2), float(self.system_manager.get_delay() + 2)))
                Printer.print(
                    '[green]{tofollow.get_handle()} is now followed by all other accounts!', timestamp=True)
                time.sleep(random.uniform(float(self.system_manager.get_delay(
                ) - 2), float(self.system_manager.get_delay() + 2)))
        except:
            pass

    def fetch_mentions(self):
        Printer.print('[white]Fetching mentions...', timestamp=True)
        isSuccess = False
        skip_counter = 0
        for account in self.accounts:
            result, skips = account.fetch_mentions()
            if not isSuccess:
                isSuccess = result
            skip_counter += skips
        Printer.print_line_center()
        if isSuccess == True:
            Printer.print(
                '[green]Mention success was detected, and has been sent to your webhook!', timestamp=True)
        else:
            Printer.print(
                '[yellow]No mention success was detected!', timestamp=True)
        if skip_counter > 0:
            Printer.print(
                f'[yellow]{str(skip_counter)} mentions were skipped due to having less than {str(self.system_manager.get_minlikes())} likes.', timestamp=True)
        Printer.print_line_center()

    def fetch_dms(self):
        Printer.print('[white]Fetching DMs...', timestamp=True)
        isSuccess = False
        for account in self.accounts:

            result = account.fetch_dms()

            if not isSuccess:
                isSuccess = result

        Printer.print_line_center()
        if isSuccess == True:
            Printer.print(
                '[green]DM success was detected, and has been sent to your webhook!', timestamp=True)
        else:
            Printer.print(
                '[yellow]No DM success was detected!', timestamp=True)
