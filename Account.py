import requests
import random
import binascii
import asyncio
import json
import datetime
import pyppeteer
import stealthy
import time
import datetime
from Printer import Printer


class Account:

    def __init__(self, system_manager, group, login, password, handle, token=None, proxy=None, write_proxy=None, Info=None):
        self.group = group
        self.login = login
        self.password = password
        self.handle = handle
        self.token = token
        self.proxy = proxy
        self.write_proxy = write_proxy
        self.Info = Info
        self.session = requests.Session()
        self.csrf = None
        self.guest = None
        self.system_manager = system_manager

    def get_group(self):
        return self.group

    def set_group(self, group):
        self.group = group

    def get_login(self):
        return self.login

    def set_login(self, login):
        self.login = login

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_handle(self):
        return self.handle

    def set_handle(self, handle):
        self.handle = handle

    def get_token(self):
        return self.token

    def set_token(self, token):
        self.token = token

    def get_proxy(self):
        return self.proxy

    def set_proxy(self, proxy):
        self.proxy = proxy

    def set_write_proxy(self, write_proxy):
        self.write_proxy = write_proxy

    def get_write_proxy(self):
        return self.write_proxy

    def get_Info(self):
        return self.Info

    def set_Info(self, Info):
        self.Info = Info

    def fetch_token(self):
        try:
            Printer.print(
                f'[yellow]Fetching token for @{self.handle}!', timestamp=True, ending=True)

            session = requests.Session()
            session.cookies.clear()
            if not self.proxy is None:
                session.proxies.update(self.proxy)
            session.get('https://twitter.com/login')

            authenticity_token = binascii.hexlify(
                random.getrandbits(16 * 8).to_bytes(16, 'big')).decode()
            cookies = {'_mb_tk': authenticity_token}
            data = {
                'redirect_after_login': '/',
                'remember_me': '1',
                'authenticity_token': authenticity_token,
                'wfa': '1',
                'ui_metrics': '{}',
                'session[username_or_email]': self.login,
                'session[password]': self.password,
            }
            response = session.post(
                "https://twitter.com/sessions", data=data, cookies=cookies)

            if '/account/login_challenge?challenge_id' in response.text:
                Printer.print(
                    f'[yellow]Your account @{self.handle} requires verification! Please complete the challenge in the browser window!', timestamp=True)

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(self.manually_fetch_token())
                finally:
                    loop.close()
                    asyncio.set_event_loop(None)

            if response.status_code == 200:
                auth_token = session.cookies.get_dict()['auth_token']
                self.token = auth_token
                Printer.print(
                    f'[green]Fetched auth token for @{self.handle}!     ', timestamp=True)

        except Exception as e:
            Printer.print(
                f'[red]Failed to fetch auth token for @{self.handle}! Please manually login in the browser window appearing.', timestamp=True)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(self.manually_fetch_token())
            finally:
                loop.close()
                asyncio.set_event_loop(None)

    async def manually_fetch_token(self):
        try:
            if self.proxy != '' and self.proxy is not None:
                front, back = self.proxy['http'].split("@")
                host, port = back.split(":")
                user, password = front.replace('http://', '').split(":")
                browser = await pyppeteer.launch({"handleSIGINT": False, "handleSIGTERM": False, "handleSIGHUP": False, 'args': ['--proxy-server=' + host + ':' + port], 'headless': False, 'defaultViewport': None, 'ignoreDefaultArgs': ['--enable-automation', "--disable-extensions"]})
            else:
                browser = await pyppeteer.launch({"handleSIGINT": False, "handleSIGTERM": False, "handleSIGHUP": False, 'headless': False, 'defaultViewport': None, 'ignoreDefaultArgs': ['--enable-automation', "--disable-extensions"]})

            page = await browser.newPage()
            await stealthy.stealth(page)

            if self.proxy != '' and self.proxy is not None:
                await page.authenticate({'username': user, 'password': password})

            cn = {
                'url': 'https://twitter.com/home',
                'value': '1',
                'name': 'eu_cn'
            }
            dark = {
                'url': 'https://twitter.com/home',
                'value': '1',
                'name': 'night_mode'
            }

            await page.setCookie(cn)
            await page.setCookie(dark)

            await page.goto('https://twitter.com/login/error?username_or_email=' + self.handle)
            main = await browser.pages()
            tab1 = main[0]
            await stealthy.stealth(tab1)
            await tab1.bringToFront()
            await tab1.goto('https://twitter.com/login/error?username_or_email=' + self.handle)
            await page.close()
            try:
                await tab1.waitForNavigation({'waitUntil': 'networkidle0'})
                username_or_email = await tab1.querySelectorAll("input[name='text']")
                if username_or_email[0]:
                    await tab1.type("input[name='text']", self.handle)
                time.sleep(2)
            except:
                pass

            Printer.input(
                "[green]Press enter when you have completed the challenge >>> ", timestamp=True)

            cookies = await tab1.cookies()
            for cookie in cookies:
                if cookie['name'] == 'auth_token':
                    self.token = cookie['value']
            await tab1.close()
            await browser.close()

        except Exception as e:
            Printer.print_error('FT01', 'Error while fetching the token!')

    async def launch_account(self):
        try:
            if self.proxy != '' and self.proxy != None:
                front, back = self.proxy['http'].split("@")
                host, port = back.split(":")
                user, password = front.replace('http://', '').split(":")
                browser = await pyppeteer.launch({"handleSIGINT": False, "handleSIGTERM": False, "handleSIGHUP": False, 'args': ['--proxy-server=' + host + ':' + port], 'headless': False, 'defaultViewport': None, 'ignoreDefaultArgs': ['--enable-automation', "--disable-extensions"]})
            else:
                browser = await pyppeteer.launch({"handleSIGINT": False, "handleSIGTERM": False, "handleSIGHUP": False, 'headless': False, 'defaultViewport': None, 'ignoreDefaultArgs': ['--enable-automation', "--disable-extensions"]})
            page = await browser.newPage()
            await stealthy.stealth(page)

            try:
                better_acc_token = self.token
                if "media-" in str(self.token).lower():
                    better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                        " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
            except:
                Printer.print(f'[red]ERROR Media token!', timestamp=True)
                pass

            if self.write_proxy != '' and self.write_proxy != None:
                await page.authenticate({'username': user, 'password': password})

            tokenCookie = {
                'url': 'https://twitter.com/home',
                'value': better_acc_token,
                'name': 'auth_token'
            }
            cn = {
                'url': 'https://twitter.com/home',
                'value': '1',
                'name': 'eu_cn'
            }
            dark = {
                'url': 'https://twitter.com/home',
                'value': '1',
                'name': 'night_mode'
            }

            await page.setCookie(cn)
            await page.setCookie(tokenCookie)
            await page.setCookie(dark)

            await page.goto('https://www.twitter.com/home')
            main = await browser.pages()
            tab1 = main[0]
            await stealthy.stealth(tab1)
            await tab1.bringToFront()
            await tab1.goto('https://www.twitter.com/home')
            await page.close()

            await tab1.waitForNavigation({'waitUntil': 'networkidle0'})
            if tab1.url == "https://twitter.com/account/access":
                try:
                    restricted = await tab1.querySelectorAll("body > div.PageContainer > div > form > input.Button.EdgeButton.EdgeButton--primary")
                    if restricted[0]:
                        await tab1.click("body > div.PageContainer > div > form > input.Button.EdgeButton.EdgeButton--primary")
                except Exception as e:
                    Printer.print(
                        f'[red]Couldnt unrestrict the account! Please solve manually.', timestamp=True)
                    Printer.input(
                        "[green]Press enter when done >>> ", timestamp=True)
                    Printer.print_line_center()
                    await tab1.close()
                    await browser.close()
                    return

                await tab1.waitForNavigation({'waitUntil': 'networkidle0'})
                try:
                    captcha = await tab1.querySelectorAll("body > div.PageContainer > div > div.PaddingBottom > form > input.Button.EdgeButton.EdgeButton--primary")
                    if len(captcha) > 0:
                        await tab1.click("body > div.PageContainer > div > div.PaddingBottom > form > input.Button.EdgeButton.EdgeButton--primary")
                        Printer.print(
                            "[red]Captcha detected! Please solve manually.", timestamp=True)
                        Printer.input(
                            "[green]Press enter when done >>> ", timestamp=True)
                        Printer.print_line_center()
                        await tab1.close()
                        await browser.close()
                        return
                except Exception as e:
                    pass

                if tab1.url.startswith("https://twitter.com/home"):
                    Printer.print(
                        f'[green]Account is no longer restricted!', timestamp=True)
                    await tab1.close()
                    await browser.close()
                    return
                else:
                    Printer.print(
                        f'[red]ERROR Couldnt unrestrict the account! Please solve manually.', timestamp=True)
                    Printer.input(
                        "[green]Press enter when done >>> ", timestamp=True)
                    Printer.print_line_center()
                    await tab1.close()
                    await browser.close()
                    return

            else:
                Printer.input(
                    "[green]Press enter when done >>> ", timestamp=True)
                Printer.print_line_center()
                await tab1.close()
                await browser.close()

        except pyppeteer.errors.NetworkError:
            pass
        except Exception as e:
            try:
                await tab1.close()
                await browser.close()
            except:
                pass
            Printer.print_error('AL01', 'Faile to launch the account!')

    def fetch_mentions(self) -> bool:
        try:
            try:
                better_acc_token = self.token
                if "media-" in str(self.token).lower():
                    better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                        " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
            except:
                Printer.print('[red]ERROR Media token! 11', timestamp=True)

            url = 'https://api.twitter.com/1.1/statuses/mentions_timeline.json?tweet_mode=extended&count=50'
            headers = {
                'x-csrf-token': self.csrf,
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'Cookie': 'personalization_id=; guest_id=' + self.guest + '; auth_token=' + better_acc_token + '; lang=en; ct0=' + self.csrf,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            r = requests.get(url, headers=headers, proxies=self.proxy)
            try:
                mentionsJson = json.loads(r.text)
                isSuccess = False
                skip_counter = 0

                for tweet in mentionsJson:
                    checker = False

                    if int(tweet["favorite_count"]) < int(self.system_manager.get_minlikes()):
                        checker = True
                        skip_counter += 1

                    try:
                        self.system_manager.get_file_manager().write_mentions(
                            {'Account': self.handle, 'Host': tweet["user"]['screen_name'], 'Link': "https://twitter.com/" + tweet["user"]['screen_name'] + "/status/" + str(tweet["id"]), 'Content': tweet['full_text'], 'Date': tweet['created_at']})
                    except:
                        pass

                    if time.strptime(tweet['created_at'], "%a %b %d %X %z %Y") > time.strptime(self.system_manager.get_file_manager().get_lastran()[self.group]['time'], "%a %b %d %X %Y"):
                        if checker == False:

                            embed = {
                                "embeds": [
                                    {
                                        "color": 12837112,
                                        "fields": [
                                            {
                                                "name": "Account:",
                                                "value": "||" + self.handle + "||",
                                                "inline": True
                                            },
                                            {
                                                "name": "From:",
                                                "value": "[" + tweet["user"]['screen_name'] + "](https://twitter.com/" + tweet["user"]['screen_name'] + ")",
                                                "inline": True
                                            },
                                            {
                                                "name": "Type:",
                                                "value": "Mention",
                                                "inline": True
                                            },
                                            {
                                                "name": "Content:",
                                                "value": tweet['full_text']
                                            },
                                            {
                                                "name": "‏‏‎ ‎",
                                                "value": "‏‏‎ ‎"
                                            },
                                            {
                                                "name": "Account Group:",
                                                "value": "||" + self.group + "||",
                                                "inline": True
                                            },
                                            {
                                                "name": "Account Proxy:",
                                                "value": "||" + self.proxy["http"] + "||",
                                                "inline": True
                                            },
                                            {
                                                "name": "‏‏‎ ‎",
                                                "value": "‏‏‎ ‎",
                                                "inline": True
                                            }
                                        ],
                                        "author": {
                                            "name": "New Success detected!",
                                            "url": "https://twitter.com/" + tweet["user"]['screen_name'] + "/status/" + str(tweet["id"]),
                                            "icon_url": "https://media.discordapp.net/attachments/789085414547914762/839796053992931338/360_F_240043850_TbiOT82A1aRJ45cwZZwQbR1ETZNRXofr.png"
                                        },
                                        "footer": {
                                            "text": "Cipher Success",
                                            "icon_url": "https://cdn.discordapp.com/avatars/775988343686168578/a25b44b8735a1679c29844964b34c255.png?size=4096"
                                        },
                                        "timestamp": str(datetime.datetime.now()),
                                        "thumbnail": {
                                            "url": str(tweet["user"]['profile_image_url']).replace("normal", "400x400")
                                        }
                                    }
                                ],
                                "username": "Cipher Success",
                                "avatar_url": "https://cdn.discordapp.com/avatars/775988343686168578/a25b44b8735a1679c29844964b34c255.png?size=4096"
                            }

                            requests.post(url=self.system_manager.get_webhook(), data=json.dumps(
                                embed), headers={"Content-Type": "application/json"})

                            data = {
                                "userid": str(self.system_manager.get_user_id()),
                                "account": self.handle,
                                "link": "https://twitter.com/" + tweet["user"]['screen_name'] + "/status/" + str(tweet["id"]),
                                "content": tweet['full_text'],
                                "g_owner": tweet["user"]['screen_name'],
                                "date": f'{datetime.datetime.now().strftime("%H:%M - %B %d, %Y")}'
                            }

                            try:

                                requests.post(
                                    f"CIPHERWATCH_URL", json=data, timeout=5)
                            except:
                                pass

                            isSuccess = True
                            Printer.print(
                                f'[green]Mention success detected for @{self.handle}! It has been sent to your webhook.', timestamp=True)
            except:
                pass
        except:
            Printer.print(
                f'[red]Error while getting mention success for @{self.handle}!', timestamp=True)

        return isSuccess, skip_counter

    def fetch_dms(self):
        isSuccess = False
        try:
            try:
                better_acc_token = self.token
                if "media-" in str(self.token).lower():
                    better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                        " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
            except:
                Printer.print('[red]ERROR Media token!', timestamp=True)

            url = 'https://twitter.com/i/api/1.1/dm/inbox_initial_state.json?tweet_mode=extended'
            headers = {
                'x-csrf-token': self.csrf,
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'Cookie': 'personalization_id=; guest_id=' + self.guest + '; auth_token=' + better_acc_token + '; lang=en; ct0=' + self.csrf,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            r = requests.get(url, headers=headers, proxies=self.proxy)
            DMjson = json.loads(r.text)
            try:
                test = DMjson['inbox_initial_state']['entries']

                for message in DMjson['inbox_initial_state']['entries']:
                    if not 'message' in message:
                        continue
                    message = message['message']
                    senderid = message['message_data']['sender_id']
                    group_dm = False
                    try:
                        recieverid = message['message_data']['recipient_id']
                    except:
                        recieverid = message['message_data']['conversation_id']
                        group_dm = True
                    handleLower = self.handle.lower()
                    senderLower = DMjson['inbox_initial_state']['users'][senderid]['screen_name'].lower(
                    )

                    try:
                        self.system_manager.get_file_manager().write_dms({'Account': str(self.handle).encode("utf-8"), 'Host': str(DMjson['inbox_initial_state']['users'][senderid]['screen_name']).encode(
                            "utf-8"), 'Content': str(message['message_data']['text']).encode("utf-8"), 'Date': str(message['message_data']['time']).encode("utf-8")})
                    except:
                        pass

                    if datetime.datetime.utcfromtimestamp(int(message['message_data']['time']) / 1e3) > datetime.datetime.utcfromtimestamp(self.system_manager.get_file_manager().get_lastran()[self.group]['timestamp'] / 1e3):
                        if not (handleLower == senderLower):
                            if group_dm:
                                author_field = {
                                    "name": "New Success detected!",
                                    "url": "https://twitter.com/messages/" + recieverid,
                                    "icon_url": "https://media.discordapp.net/attachments/789085414547914762/839796053992931338/360_F_240043850_TbiOT82A1aRJ45cwZZwQbR1ETZNRXofr.png"
                                }
                            else:
                                author_field = {
                                    "name": "New Success detected!",
                                    "url": "https://twitter.com/messages/" + recieverid + "-" + senderid,
                                    "icon_url": "https://media.discordapp.net/attachments/789085414547914762/839796053992931338/360_F_240043850_TbiOT82A1aRJ45cwZZwQbR1ETZNRXofr.png"
                                }

                            embed = {
                                "embeds": [
                                    {
                                        "color": 12837112,
                                        "fields": [
                                            {
                                                "name": "Account:",
                                                "value": "||" + self.handle + "||",
                                                "inline": True
                                            },
                                            {
                                                "name": "From:",
                                                "value": "[" + DMjson['inbox_initial_state']['users'][senderid]['screen_name'] + "](https://twitter.com/" + DMjson['inbox_initial_state']['users'][senderid]['screen_name'] + ")",
                                                "inline": True
                                            },
                                            {
                                                "name": "Type:",
                                                "value": "DM",
                                                "inline": True
                                            },
                                            {
                                                "name": "Content:",
                                                "value": message['message_data']['text']
                                            },
                                            {
                                                "name": "‏‏‎ ‎",
                                                "value": "‏‏‎ ‎"
                                            },
                                            {
                                                "name": "Account Group:",
                                                "value": "||" + self.group + "||",
                                                "inline": True
                                            },
                                            {
                                                "name": "Account Proxy:",
                                                "value": "||" + self.proxy["http"] + "||",
                                                "inline": True
                                            },
                                            {
                                                "name": "‏‏‎ ‎",
                                                "value": "‏‏‎ ‎",
                                                "inline": True
                                            }
                                        ],
                                        "author": author_field,
                                        "footer": {
                                            "text": "Cipher Success",
                                            "icon_url": "https://cdn.discordapp.com/avatars/775988343686168578/a25b44b8735a1679c29844964b34c255.png?size=4096"
                                        },
                                        "timestamp": str(datetime.datetime.now()),
                                        "thumbnail": {
                                            "url": str(DMjson['inbox_initial_state']['users'][senderid]['profile_image_url']).replace("normal", "400x400")
                                        }
                                    }
                                ],
                                "username": "Cipher Success",
                                "avatar_url": "https://cdn.discordapp.com/avatars/775988343686168578/a25b44b8735a1679c29844964b34c255.png?size=4096"
                            }

                            requests.post(url=self.system_manager.get_webhook(), data=json.dumps(
                                embed), headers={"Content-Type": "application/json"})

                            data = {
                                "userid": str(self.system_manager.get_user_id()),
                                "account": self.handle,
                                "link": "dm",
                                "content": message['message_data']['text'],
                                "g_owner": DMjson['inbox_initial_state']['users'][senderid]['screen_name'],
                                "date": f'{datetime.datetime.now().strftime("%H:%M - %B %d, %Y")}'
                            }

                            try:

                                requests.post(
                                    f"CIPHERWATCH_URL", json=data, timeout=5)
                            except:
                                pass

                            isSuccess = True
                            Printer.print(
                                f'[green]DM success detected for @{self.handle}! It has been sent to your webhook.')
            except:
                pass
        except:
            Printer.print(
                f'[red]Error while getting DM success for @{self.handle}!')

        return isSuccess

    def prepare(self) -> bool:
        try:
            try:
                better_acc_token = self.token
                if "media-" in str(self.token).lower():
                    better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                        " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
            except:
                Printer.print('[red]ERROR Media token', timestamp=True)
            try:
                headers = {
                    'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                    'x-csrf-token': '',
                    'Cookie': 'personalization_id=; guest_id=; auth_token=' + better_acc_token + '; lang=en; ct0=7',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                }
                r = requests.get(
                    'https://api.twitter.com/1.1/lists/subscriptions.json', headers=headers, proxies=self.proxy)
            except Exception as e:
                Printer.print(
                    f'[red]Error while preparing @{self.handle}! The account will not be ran...', timestamp=True)
                return False

            cookies = r.cookies
            self.guest = cookies['guest_id']
            self.csrf = cookies['ct0']
            headers = {
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'x-csrf-token': cookies["ct0"],
                'Cookie': 'personalization_id=; guest_id=; auth_token=' + better_acc_token + '; lang=en; ct0=' + cookies["ct0"],
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            }
            r = requests.get(
                'https://api.twitter.com/1.1/lists/subscriptions.json', headers=headers, proxies=self.proxy)

            if r.text == '{"errors":[{"code":32,"message":"Could not authenticate you."}]}':
                Printer.print(
                    f'[yellow]Account Token for @{self.handle} is outdated. The bot will try to fetch a new token...', timestamp=True)
                self.fetch_token()
                self.system_manager.get_file_manager().update_account(self)
                return self.prepare()
            if r.text == '{"errors":[{"code":64,"message":"Your account is suspended and is not permitted to access this feature."}]}':
                Printer.print(
                    f'[red]The account {self.handle} is suspended, and will not be ran.')

                data = {
                    "userid": str(self.system_manager.get_user_id()),
                    "account": self.handle,
                    "mode": "suspended",
                    "date": f'{datetime.datetime.now().strftime("%H:%M - %B %d, %Y")}'
                }
                try:
                    requests.post(
                        f"CIPHERWATCH_URL", json=data, timeout=5)
                except:
                    pass

                self.info = 'suspended'
                return False

            elif r.text == '{"errors":[{"code":326,"message":"To protect our users from spam and other malicious activity, this account is temporarily locked. Please log in to https://twitter.com to unlock your account.","sub_error_code":0,"bounce_location":"https://twitter.com/account/access"}]}':
                Printer.print(
                    f'[yellow]The account {self.handle} is restricted. A browser is being opened to verify. Please complete the challenge!')

                data = {
                    "userid": str(self.system_manager.get_user_id()),
                    "account": self.handle,
                    "mode": "restricted",
                    "date": f'{datetime.datetime.now().strftime("%H:%M - %B %d, %Y")}'
                }

                try:
                    requests.post(
                        f"CIPHERWATCH_URL", json=data, timeout=5)
                except:
                    pass

                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(self.launch_account())
                finally:
                    loop.close()
                    asyncio.set_event_loop(None)
                return True
            else:
                Printer.print(
                    '                                                      ', ending=True)
                Printer.print(
                    f'[green]Prepared @{self.handle}!', timestamp=True, ending=True)
                return True
        except Exception as e:
            Printer.print(
                f'[red]Error while preparing @{self.handle}!', timestamp=True)
            return False

    def comment_post(self, id, name, link, comment, media, quote):
        try:
            try:
                better_acc_token = self.token
                if "media-" in str(self.token).lower():
                    better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                        " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
            except:
                Printer.print(f'[red]ERROR Media token', timestamp=True)

            url = 'https://twitter.com/i/api/1.1/statuses/update.json'
            headers = {
                'x-csrf-token': self.csrf,
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'Cookie': 'personalization_id=; guest_id=' + self.guest + '; auth_token=' + better_acc_token + '; lang=en; ct0=' + self.csrf,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            if media == None and quote == None:
                payload = {'auto_populate_reply_metadata': 'true',
                           'in_reply_to_status_id': id, 'status': comment}
            elif media == None and quote != None:
                payload = {'auto_populate_reply_metadata': 'true',
                           'status': comment, 'attachment_url': quote}
            else:
                payload = {'auto_populate_reply_metadata': 'true',
                           'in_reply_to_status_id': id, 'status': comment, 'media_ids': [str(media)]}
            r = requests.post(url, headers=headers,
                              data=payload, proxies=self.proxy)
            if r.status_code != 200:
                if r.text == '{"errors":[{"code":187,"message":"Status is a duplicate."}]}':
                    Printer.print("[red]Failed to comment " + ' in a giveaway by @' + name + ' - Link: ' + link +
                                  ' - Account: ' + self.handle + " - Reason: Duplicate comment by the same account", timestamp=True)
                    return False
                else:
                    Printer.print("[red]Failed to comment " + ' in a giveaway by @' +
                                  name + ' - Link: ' + link + ' - Account: ' + self.handle)
                    return False
            else:
                Printer.print(
                    "                                                                                                    ", ending=True)
                return True
        except Exception as e:
            Printer.print("[red]Failed to comment " + ' in a giveaway by @' + name + ' - Link: ' + link +
                          ' - Account: ' + self.handle, timestamp=True)
            return False

    def upload_media(self, media):
        try:
            try:
                better_acc_token = self.token
                if "media-" in str(self.token).lower():
                    better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                        " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
            except:
                Printer.print(f'[red]ERROR Media token', timestamp=True)

            url = 'https://upload.twitter.com/1.1/media/upload.json'
            headers = {
                'x-csrf-token': self.csrf,
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'Cookie': 'personalization_id=; guest_id=' + self.guest + '; auth_token=' + better_acc_token + '; lang=en; ct0=' + self.csrf,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            payload = {'media_category': 'tweet_image', 'media_data': media}
            r = requests.post(url, headers=headers,
                              data=payload, proxies=self.proxy)
            check = json.loads(r.text)
            if r.status_code != 200:
                Printer.print(
                    "[red]Failed to upload image to Twitter", timestamp=True)
                return None
            else:
                Printer.print(
                    "                                                                                                    ", ending=True)
                return check['media_id_string']
        except Exception as e:
            Printer.print(
                "[red]Failed to upload image to Twitter", timestamp=True)
            return None

    def retweet_post(self, id, name, link):
        try:
            try:
                better_acc_token = self.token
                if "media-" in str(self.token).lower():
                    better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                        " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
            except:
                Printer.print(f'[red]ERROR Media token', timestamp=True)

            url = 'https://twitter.com/i/api/1.1/statuses/retweet.json'
            headers = {
                'x-csrf-token': self.csrf,
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'Cookie': 'personalization_id=; guest_id=' + self.guest + '; auth_token=' + better_acc_token + '; lang=en; ct0=' + self.csrf,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            payload = 'id=' + id
            r = requests.post(url, headers=headers,
                              data=payload, proxies=self.proxy)
            check = json.loads(r.text)
            if r.status_code != 200 or check['retweeted_status']['id_str'] != id:
                if r.text == '{"errors":[{"code":327,"message":"You have already retweeted this Tweet."}]}':
                    Printer.print("[yellow]A giveaway by @" + name + ' for @' + self.handle +
                                  " has already been ran and will be skipped.", timestamp=True)
                    Printer.print(
                        "                                                                                                    ", ending=True)
                    return "SKIP"
                else:
                    Printer.print("[red]Failed to retweet a giveaway by @" + name +
                                  ' - Link: ' + link + ' - Account: ' + self.handle, timestamp=True)
                    return False

            else:
                Printer.print(
                    "                                                                                                    ", ending=True)
                return True
        except:
            Printer.print("[red]Failed to retweet a giveaway by @" + name +
                          ' - Link: ' + link + ' - Account: ' + self.handle, timestamp=True)
            return False

    def like_post(self, id, name, link):
        try:
            try:
                better_acc_token = self.token
                if "media-" in str(self.token).lower():
                    better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                        " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
            except:
                Printer.print(f'[red]ERROR Media token', timestamp=True)

            url = 'https://twitter.com/i/api/1.1/favorites/create.json'
            headers = {
                'x-csrf-token': self.csrf,
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'Cookie': 'personalization_id=; guest_id=' + self.guest + '; auth_token=' + better_acc_token + '; lang=en; ct0=' + self.csrf,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            payload = 'id=' + id
            r = requests.post(url, headers=headers,
                              data=payload, proxies=self.proxy)
            check = json.loads(r.text)
            if r.status_code != 200 or check['id_str'] != id:
                if r.text == '{"errors":[{"code":139,"message":"You have already favorited this status."}]}':
                    Printer.print("[yellow]A giveaway by @" + name + ' for @' + self.handle +
                                  " has already been ran and will be skipped.", timestamp=True)
                    Printer.print(
                        "                                                                                                    ", ending=True)
                    return "SKIP"
                else:
                    Printer.print("[red]Failed to like a giveaway by @" + name +
                                  ' - Link: ' + link + ' - Account: ' + self.handle, timestamp=True)
                    return False
            else:
                Printer.print(
                    "                                                                                                    ", ending=True)
                return True
        except:
            Printer.print("[red]Failed to like a giveaway by @" + name +
                          ' - Link: ' + link + ' - Account: ' + self.handle, timestamp=True)
            return False

    def follow_account(self, id, name, link):
        try:
            try:
                better_acc_token = self.token
                if "media-" in str(self.token).lower():
                    better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                        " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
            except:
                Printer.print(f'[red]ERROR Media token', timestamp=True)

            url = 'https://twitter.com/i/api/1.1/friendships/create.json'
            headers = {
                'x-csrf-token': self.csrf,
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'Cookie': 'personalization_id=; guest_id=' + self.guest + '; auth_token=' + better_acc_token + '; lang=en; ct0=' + self.csrf,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            payload = 'id=' + id
            r = requests.post(url, headers=headers,
                              data=payload, proxies=self.proxy)
            check = json.loads(r.text)
            if r.status_code != 200 or check['id_str'] != id:
                Printer.print("[red]Failed to follow the giveaway host @" + name +
                              "! - Link: " + link + " - Account: " + self.handle, timestamp=True)
                return False
            else:
                Printer.print(
                    "                                                                                                    ", ending=True)
                return True
        except Exception as e:
            Printer.print("[red]Failed to follow the giveaway host @" + name +
                          "! - Link: " + link + " - Account: " + self.handle, timestamp=True)
            return False

    def follow_user_by_screenname(self, screen_name):
        try:
            better_acc_token = self.token
            if "media-" in str(self.token).lower():
                better_acc_token = str(str(self.token).lower().split("auth_token")[1].split("value")[1].split("}")[0]).replace(
                    " ", "").replace(":", "").replace("}", "").replace("{", "").replace("'", "").replace('"', "")
        except:
            Printer.print(f'[red]ERROR Media token', timestamp=True)

        url = 'https://api.twitter.com/1.1/friendships/create.json'
        headers = {
            'x-csrf-token': self.csrf,
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'Cookie': 'personalization_id=; guest_id=' + self.guest + '; auth_token=' + better_acc_token + '; lang=en; ct0=' + self.csrf,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        payload = 'screen_name=' + screen_name
        r = requests.post(url, headers=headers,
                          data=payload, proxies=self.proxy)

        if r.status_code != 200:
            Printer.print(
                f'[red]Failed to follow an account: {screen_name} - On your Account: {self.handle}', timestamp=True)
            time.sleep(random.uniform(float(self.system_manager.get_delay(
            ) - 2), float(self.system_manager.get_delay() + 2)))
        else:
            Printer.print(
                '                                                                                                    ', ending=True)
            Printer.print(
                f'[green]{self.handle} followed {screen_name}', timestamp=True, ending=True)
            time.sleep(random.uniform(float(self.system_manager.get_delay(
            ) - 2), float(self.system_manager.get_delay() + 2)))
