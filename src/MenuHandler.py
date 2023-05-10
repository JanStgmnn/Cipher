from Printer import Printer
import os
import asyncio
import requests
import time
from playsound import playsound


class MenuHandler:

    def __init__(self, system_manager):
        self.system_manager = system_manager
        self.file_manager = self.system_manager.get_file_manager()
        self.twitter = self.system_manager.get_twitter()
        self.account_manager = self.system_manager.get_account_manager()
        self.discord = self.system_manager.get_discord()

    def main_menu(self, clear=False):
        self.discord.update_rich_presence("In Main Menu", show_twitter=False)
        self.system_manager.set_title(
            "Cipher - Version " + self.system_manager.get_version())
        asyncio.set_event_loop(asyncio.new_event_loop())

        if clear:
            os.system('cls')
            Printer.print_logo()
            Printer.print_line_upper()
            Printer.print("[white]Welcome back [cyan]" + self.system_manager.get_name() + "[white]![cyan]" + (
                33-len(self.system_manager.get_name()))*" " + self.system_manager.get_version(), timestamp=True)

            if self.system_manager.get_update_available():
                Printer.print(
                    "[yellow]There is a new update available! Please restart your bot.", timestamp=True)
            else:
                Printer.print(
                    "[green]You are using the latest version.", timestamp=True)

            self.system_manager.admin_message()

        Printer.print_line_center()
        Printer.print("[magenta]What do you want to do?", timestamp=True)
        Printer.print("[white]1) Start the Twitter Module", timestamp=True)
        Printer.print("[white]2) Check for Success", timestamp=True)
        Printer.print("[white]3) Login to Accounts", timestamp=True)
        Printer.print("[white]4) Utils", timestamp=True)
        Printer.print("[magenta]X) [white]Close the Bot", timestamp=True)
        answer = Printer.input('[white]> ', timestamp=True)

        if answer == '1':
            self.discord.update_rich_presence(
                "Entering Giveaways", show_twitter=True)
            self.twitter.run_setup()
            self.system_manager.get_file_manager().load_time()
            try:
                requests.post(f"LAST_USED_API", params={"user": self.system_manager.get_user_id(), "type": self.system_manager.get_user_type(
                ), "date": str(int(time.time()))},
                    headers={'Authorization': 'BEARER'})
            except:
                pass
            self.twitter.run_twitter()
            self.account_manager.fetch_mentions()
            self.account_manager.fetch_dms()
            self.system_manager.get_file_manager().update_time()
            try:
                playsound("https://cipher-bots.com/static/cipher/sound.mp3")
            except:
                pass
            self.main_menu(True)
        elif answer == '2':
            self.discord.update_rich_presence(
                "Checking for Success", show_twitter=True)
            self.twitter.run_setup()
            self.account_manager.prepare_accounts()
            self.system_manager.get_file_manager().load_time()
            self.account_manager.fetch_mentions()
            self.account_manager.fetch_dms()
            self.system_manager.get_file_manager().update_time()
            self.main_menu(True)

        elif answer == '3':
            self.discord.update_rich_presence(
                "Managing Accounts", show_twitter=True)
            self.twitter.run_setup()
            self.account_manager.prepare_accounts()
            self.accounts_menu()
            self.main_menu(True)

        elif answer == '4':
            self.discord.update_rich_presence(
                "Editing settings", show_twitter=True)
            self.utils_menu(True)

        elif answer.lower() == 'x':
            os._exit(0)
        else:
            Printer.print(
                "[red]Wrong input! Please try again.", timestamp=True)
            self.main_menu(True)

    def accounts_menu(self):
        if len(self.account_manager.get_accounts()) > 0:
            while True:
                Printer.print(
                    "[magenta]Which account do you want to login to?", timestamp=True)
                for account in self.account_manager.get_accounts():
                    Printer.print("[white]" + str(self.account_manager.get_accounts().index(
                        account)) + ") @" + account.get_handle(), timestamp=True)
                Printer.print(
                    "[magenta]X) [white]Return to Main Menu", timestamp=True)
                answer = Printer.input('[white]> ', timestamp=True)
                try:
                    if answer.lower() == 'x':
                        break
                    else:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        try:
                            loop.run_until_complete(self.account_manager.get_accounts()[
                                                    int(answer)].launch_account())
                        finally:
                            loop.close()
                            asyncio.set_event_loop(None)
                        self.accounts_menu()
                        break
                except:
                    Printer.print(
                        "[red]Invalid account. Please try again.", timestamp=True)
        else:
            Printer.print(
                "[red]You have no valid accounts to login to!", timestamp=True)

    def settings_menu(self):
        os.system('cls')
        Printer.print_logo()
        Printer.print_line_upper()
        Printer.print("[white]Welcome back [cyan]" + self.system_manager.get_name() + "[white]![cyan]" + (
            33-len(self.system_manager.get_name()))*" " + self.system_manager.get_version(), timestamp=True)
        if self.system_manager.get_update_available():
            Printer.print(
                "[yellow]There is a new update available! Please restart your bot.", timestamp=True)
        else:
            Printer.print(
                "[green]You are using the latest version.", timestamp=True)

        self.system_manager.admin_message()

        Printer.print_line_center()
        Printer.print(
            "[magenta]Which setting should be changed?", timestamp=True)
        Printer.print("[white]1) Key:           [cyan]" +
                      self.system_manager.get_key(), timestamp=True)
        Printer.print("[white]2) Delay:         [cyan]" +
                      str(self.system_manager.get_delay()), timestamp=True)
        Printer.print("[white]3) Webhook:       [cyan]" +
                      self.system_manager.get_webhook(), timestamp=True)
        Printer.print("[white]4) Error Webhook: [cyan]" +
                      self.system_manager.get_error_webhook(), timestamp=True)
        Printer.print("[white]5) 2 Captcha Key: [cyan]" +
                      self.system_manager.get_capkey().replace("\n", ""), timestamp=True)
        Printer.print("[white]6) Minimum Likes: [cyan]" +
                      str(self.system_manager.get_minlikes()), timestamp=True)
        Printer.print("[magenta]X) [white]Go back", timestamp=True)
        answer = Printer.input("[white]> ", timestamp=True)

        Printer.print_line_center()

        if answer == '1':
            Printer.print("[magenta]Please enter the new key:", timestamp=True)
            key = Printer.input("[white]> ", timestamp=True)
            self.system_manager.set_key(key)
            self.system_manager.get_file_manager().save_settings()
            self.settings_menu()

        elif answer == '2':
            Printer.print(
                "[magenta]Please enter the new delay:", timestamp=True)
            delay = Printer.input("[white]> ", timestamp=True)
            if int(delay) < 2:
                Printer.print(
                    '[red]Your delay is to low, please increase it to 2 or higher!', timestamp=True)
                self.settings_menu()
            self.system_manager.set_delay(int(delay))
            self.system_manager.get_file_manager().save_settings()
            self.settings_menu()

        elif answer == '3':
            Printer.print(
                "[magenta]Please enter the new webhook:", timestamp=True)
            webhook = Printer.input("[white]> ", timestamp=True)
            self.system_manager.set_webhook(webhook)
            self.system_manager.get_file_manager().save_settings()
            self.settings_menu()

        elif answer == '4':
            Printer.print(
                "[magenta]Please enter the new error webhook:", timestamp=True)
            error_webhook = Printer.input("[white]> ", timestamp=True)
            self.system_manager.set_error_webhook(error_webhook)
            self.system_manager.get_file_manager().save_settings()
            self.settings_menu()

        elif answer == '5':
            Printer.print(
                "[magenta]Please enter the new 2captcha key:", timestamp=True)
            capkey = Printer.input("[white]> ", timestamp=True)
            self.system_manager.set_capkey(capkey)
            self.system_manager.get_file_manager().save_settings()
            self.settings_menu()

        elif answer == '6':
            Printer.print(
                "[magenta]Please enter the new minimum likes:", timestamp=True)
            minlikes = Printer.input("[white]> ", timestamp=True)
            self.system_manager.set_minlikes(int(minlikes))
            self.system_manager.get_file_manager().save_settings()
            self.settings_menu()

        elif answer.lower() == 'x':
            self.utils_menu(True)

    def utils_menu(self, clear=False):
        if clear:
            os.system('cls')
            Printer.print_logo()
            Printer.print_line_upper()
            Printer.print("[white]Welcome back [cyan]" + self.system_manager.get_name() + "[white]![cyan]" + (
                33-len(self.system_manager.get_name()))*" " + self.system_manager.get_version(), timestamp=True)
            if self.system_manager.get_update_available():
                Printer.print(
                    "[yellow]There is a new update available! Please restart your bot.", timestamp=True)
            else:
                Printer.print(
                    "[green]You are using the latest version.", timestamp=True)

            self.system_manager.admin_message()

        Printer.print_line_center()
        Printer.print("[magenta]What do you want to do?", timestamp=True)
        Printer.print("[white]1) Edit [cyan]Settings",
                      timestamp=True)
        Printer.print("[white]2) Edit [cyan]Accounts [white]File",
                      timestamp=True)
        Printer.print("[white]3) Import [cyan]Accounts", timestamp=True)
        Printer.print("[white]4) Edit [cyan]Links [white]File", timestamp=True)
        Printer.print("[white]5) Edit [cyan]Random Comments", timestamp=True)
        Printer.print("[white]6) Edit [cyan]Random Images", timestamp=True)
        Printer.print("[white]7) Follow [cyan]all accounts", timestamp=True)
        Printer.print("[white]8) Test [cyan]Proxies", timestamp=True)
        Printer.print("[white]9) Test [cyan]Webhook", timestamp=True)
        Printer.print(
            "[white]10) Send files to Support (Only run when asked to)", timestamp=True)
        Printer.print("[magenta]X) [white]Go back", timestamp=True)
        answer = Printer.input('[white]> ', timestamp=True)

        self.system_manager.re_auth()

        if answer == '1':

            self.settings_menu()

        elif answer == '2':
            self.file_manager.open_file('accounts')
            Printer.input('[green]Press enter when done >>> ', timestamp=True)
            self.utils_menu(True)

        elif answer == '3':
            self.file_manager.import_accounts()
            self.utils_menu(True)

        elif answer == '4':
            self.file_manager.open_file('links')
            Printer.input('[green]Press enter when done >>> ', timestamp=True)
            self.utils_menu(True)

        elif answer == '5':
            self.file_manager.open_file('comments')
            Printer.input('[green]Press enter when done >>> ', timestamp=True)
            self.utils_menu(True)

        elif answer == '6':
            self.file_manager.open_file('images')
            Printer.input('[green]Press enter when done >>> ', timestamp=True)
            self.utils_menu(True)

        elif answer == '7':
            self.twitter.run_setup()
            self.account_manager.prepare_accounts()
            self.account_manager.follow_other_accounts()
            self.utils_menu(True)

        elif answer == '8':
            self.twitter.check_proxies()
            self.utils_menu(True)

        elif answer == '9':
            self.discord.test_webhook()
            self.utils_menu(True)

        elif answer == '10':
            self.file_manager.send_files_to_support()
            self.utils_menu(True)

        elif answer.lower() == 'x':
            self.main_menu(True)
        else:
            Printer.print(
                "[red]Wrong input! Please try again.", timestamp=True)
            self.utils_menu(True)
