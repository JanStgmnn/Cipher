import logging
import urllib
import requests
import time
import os
import ctypes
import whop
import progressbar
import datetime
import urllib.request
from FileManager import FileManager
from Printer import Printer
from AccountManager import AccountManager
from Discord import Discord
from MenuHandler import MenuHandler
from Twitter import Twitter


class SystemManager:
    def __init__(self):
        self.version = "open-source"
        logging.disable(logging.CRITICAL)

        self.file_manager = FileManager(self)
        self.account_manager = AccountManager(self)
        self.discord = Discord(self)
        self.twitter_manager = Twitter(self)
        self.menu_handler = MenuHandler(self)

        self.key, self.delay, self.webhook, self.error_webhook, self.capkey, self.minlikes = self.file_manager.load_settings()
        self.member_name = None
        self.user_id = None
        self.user_type = None
        self.update_available = False

    def get_file_manager(self):
        return self.file_manager

    def get_account_manager(self):
        return self.account_manager

    def get_background_worker(self):
        return self.background_worker

    def get_discord(self):
        return self.discord

    def get_menu_handler(self):
        return self.menu_handler

    def get_twitter(self):
        return self.twitter_manager

    def startup(self):
        os.system('cls')
        self.set_title("Cipher - Version " + self.version)
        Printer.print_logo()
        Printer.print_line_upper()

        self.validate_key()
        self.update_bot()

        self.admin_message()

        self.discord.start_richt_presence()

        self.menu_handler.main_menu()

    def get_error_webhook(self):
        return self.error_webhook

    def get_webhook(self):
        return self.webhook

    def get_user_type(self):
        return self.user_type

    def set_key(self, key):
        self.key = key

    def set_minlikes(self, minlikes):
        self.minlikes = minlikes

    def set_error_webhook(self, webhook):
        self.error_webhook = webhook

    def get_capkey(self):
        return self.capkey

    def set_capkey(self, capkey):
        self.capkey = capkey

    def set_webhook(self, webhook):
        self.webhook = webhook

    def set_delay(self, delay):
        self.delay = delay

    def get_update_available(self):
        return self.update_available

    def set_update_available(self, value):
        self.update_available = value

    def get_version(self):
        return self.version

    def get_key(self):
        return self.key

    def get_name(self):
        return self.member_name

    def get_delay(self):
        return self.delay

    def get_minlikes(self):
        return self.minlikes

    def get_user_id(self):
        return self.user_id

    def validate_key(self):
        whop_bearer = "WHOP_BEARER"
        client = whop.Whop(bearer=whop_bearer)

        response = client.validate_license_by_key(str(self.key), {})
        if "valid" in response:
            self.member_name = response['discord']['username'].split("#")[0]
            Printer.print(
                f'[white]Welcome back [cyan]{self.member_name} [white]![cyan]{(33-len(self.member_name))*" "}{self.version}', timestamp=True)

            self.user_id = response['discord']['discord_account_id']
            self.user_type = response['plan']['title'].lower()
        else:
            Printer.print('[red]Authentication failed!', timestamp=True)
            inpt = Printer.input('Enter new Key: ', timestamp=True)

            if inpt == "":
                Printer.print('[red]No new key entered!', timestamp=True)
                self.kill_system(5)

            else:
                self.file_manager.replace_key(inpt)
                self.key = inpt

                Printer.print(
                    '[green]Your key has been updated!', timestamp=True)
                self.validate_key()

    def re_auth(self):

        whop_bearer = "WHOP_BEARER"
        client = whop.Whop(bearer=whop_bearer)

        response = client.validate_license_by_key(str(self.key), {})
        if "valid" in response:
            pass
        else:
            Printer.print('[red]You have been logged out!', timestamp=True)
            self.kill_system(10)

    def update_bot(self):
        Printer.print('[yellow]Looking for updates...',
                      ending=True, timestamp=True)

        self.file_manager.validate_structure()

        try:
            res = requests.get(
                f'UPDATE_API')
        except:
            return
        if (res.status_code == 200):
            Printer.print(
                '                                       ', ending=True)
            Printer.print('[yellow]Downloading new update...',
                          ending=True, timestamp=True)
            r = urllib.request.urlopen(res.text)
            newName = str(r.info()).split('filename="')[1].split('"')[0]
            try:
                urllib.request.urlretrieve(
                    res.text, self.file_manager.get_default_path() / newName, self.show_progress)
                self.file_manager.create_shortcut(newName)
                Printer.print(
                    '                                       ', ending=True)
                Printer.print(
                    '[green]Download complete! Please run the new version!', timestamp=True)
                self.kill_system(5)
            except:
                Printer.print(
                    '                                       ', ending=True)
                Printer.print(
                    '[red]Failed to download! Please retry!', timestamp=True)
                self.kill_system(5)
        else:
            Printer.print(
                '                                       ', ending=True)
            Printer.print(
                '[green]You are using the latest version!', timestamp=True)

    def show_progress(self, block_num, block_size, total_size):

        pbar = None

        widgets = ["  " + str(Printer.get_color('white')) + str(Printer.get_color('bright')) + datetime.datetime.now().strftime("%H:%M:%S") + str(Printer.get_color('cyan')) + ' │ ' + str(Printer.get_color('yellow')),
                   progressbar.Percentage(),
                   progressbar.Bar(),
                   ' (', progressbar.AdaptiveETA(), ') ',
                   ]

        if pbar is None:
            pbar = progressbar.ProgressBar(
                maxval=total_size, term_width=86, widgets=widgets)
            pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            pbar.update(downloaded)
        else:
            pbar.finish()
            pbar = None

    def admin_message(self):
        try:
            res = requests.get(f'ADMIN_MESSAGE_API')
        except:
            return
        if (res.status_code == 200):
            if not res.json()["adminMessage"] == "":
                Printer.print_line_center()
                Printer.print("[yellow]Admin Message:", timestamp=True)
                Printer.print("[yellow]" + res.json()
                              ["adminMessage"], timestamp=True)

    def set_title(self, title):
        ctypes.windll.kernel32.SetConsoleTitleW(title)

    @staticmethod
    def kill_system(wait_time=0):
        time.sleep(wait_time)
        os._exit(0)
