""" module imports """
import time
import json
import requests
from pypresence import Presence
from Printer import Printer


class Discord:
    '''
    This class is used for Discord related functions.
        :param system_manager: Used to run system related functions
        :type system_manager: SystemManager
        :ivar system_manager: This is where we store system_manager
        :vartype system_manager: SystemManager
    '''

    def __init__(self, system_manager):
        self.rpctime = time.time()
        self.rpc = None
        self.system_manager = system_manager

    def start_richt_presence(self):
        '''
        Starts the rich presence for Discord

        Parameters:

        Returns:
        '''

        try:
            self.rpc = Presence(client_id="PRESENCE_ID")
            self.rpc.connect()
            self.update_rich_presence("In Main Menu...", show_twitter=False)
        except:
            pass

    def update_rich_presence(self, text, show_twitter=False, show_entry=False, counter={}):
        '''
        Updates the rich presence for Discord

        Parameters:
            text (str): The text to display in the rich presence
            show_twitter (bool): Whether or not to show the twitter icon
            show_entry (bool): Whether or not to show the entry count
            counter (dict): The counter to show

        Returns:
        '''

        if show_twitter:
            try:
                self.rpc.update(
                    large_image="cipherhead",
                    small_image="twitter-new",
                    details=self.system_manager.get_version(),
                    state=str(text),
                    start=int(self.rpctime)
                )
            except:
                pass
        elif show_entry:
            try:
                self.rpc.update(
                    large_image="cipherhead",
                    small_image="twitter-new",
                    details=self.system_manager.get_version(),
                    state="Entering",
                    party_size=[counter["current"], counter["max"]],
                    start=int(self.rpctime)
                )
            except:
                pass
        else:
            try:
                self.rpc.update(
                    large_image="cipherhead",
                    details=self.system_manager.get_version(),
                    state=str(text),
                    start=int(self.rpctime)
                )
            except:
                pass

    def test_webhook(self):
        '''
        Tests the webhook to make sure it is valid

        Parameters:

        Returns:
        '''

        Printer.print(
            '[green]Sending a test webhook. Please check your webhook channel!', timestamp=True)
        try:
            embed = {
                "embeds": [
                    {
                        "title": "Your Webhook Is Working! :partying_face:",
                        "description":
                            "Your webhook is set up! Now you can start winning giveaways!",
                        "color": 4961603,
                        "footer": {
                            "text": "CipherBots",
                            "icon_url":
                                "https://cdn.discordapp.com/avatars/775988343686168578/a25b44b8735a1679c29844964b34c255.png?size=4096"
                        }
                    }
                ],
                "username": "Cipher",
                "avatar_url":
                    "https://cdn.discordapp.com/avatars/775988343686168578/a25b44b8735a1679c29844964b34c255.png?size=4096"
            }
            request = requests.post(url=self.system_manager.get_webhook(), data=json.dumps(
                embed), headers={"Content-Type": "application/json"})

            if not self.system_manager.get_error_webhook() == "":
                embed = {
                    "embeds": [
                        {
                            "title": "Your Webhook Is Working! :partying_face:",
                            "description":
                                "Your webhook is set up! Now you can start winning giveaways!",
                            "color": 4961603,
                            "footer": {
                                "text": "CipherBots",
                                "icon_url":
                                    "https://cdn.discordapp.com/avatars/775988343686168578/a25b44b8735a1679c29844964b34c255.png?size=4096"
                            }
                        }
                    ],
                    "username": "Cipher",
                    "avatar_url":
                        "https://cdn.discordapp.com/avatars/775988343686168578/a25b44b8735a1679c29844964b34c255.png?size=4096"
                }
                request = requests.post(url=self.system_manager.get_error_webhook(), data=json.dumps(
                    embed), headers={"Content-Type": "application/json"})

            try:
                request.raise_for_status()
            except requests.exceptions.HTTPError as err:
                Printer.print("  " + err)
        except:
            Printer.print(
                '[red]Please provide a webhook in your webhook.txt file!', timestamp=True)

    def send_webhook(self, embed, webhook_url=None):
        '''
        Sends a webhook to discord

        Parameters:
            embed (dict): The embed to send
            webhook_url (str): The webhook url to send to

        Returns:
        '''

        if webhook_url is None:
            webhook_url = self.system_manager.get_webhook()
        requests.post(url=webhook_url, data=json.dumps(
            embed), headers={"Content-Type": "application/json"})
