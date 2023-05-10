import random
import time
import datetime
from Printer import Printer
import requests
import json
import tweepy
from fake_headers import Headers

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
BEARER = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""


class SkipException(Exception):
    pass


class Twitter:

    def __init__(self, system_manager):
        self.valid_links = []
        self.links = []
        self.system_manager = system_manager
        self.account_manager = self.system_manager.get_account_manager()
        self.file_manager = self.system_manager.get_file_manager()
        self.discord = self.system_manager.get_discord()
        self.tweepy_client = tweepy.Client(bearer_token=BEARER, consumer_key=CONSUMER_KEY,
                                           consumer_secret=CONSUMER_SECRET, access_token=OAUTH_TOKEN, access_token_secret=OAUTH_TOKEN_SECRET)

    def run_setup(self, group=None):
        self.valid_links.clear()
        self.links.clear()
        self.account_manager.load_accounts(group)

    def run_twitter(self):
        Printer.print_line_center()
        self.collect_data()
        self.account_manager.prepare_accounts()
        self.enter_giveaways()
        self.system_manager.set_title(
            "Cipher - Version " + self.system_manager.get_version())

    def enter_giveaways(self):
        accounts = self.account_manager.get_accounts()

        giveaway_counter = 0
        entries_counter = 0

        for link in self.valid_links:
            giveaway_counter += 1

            try:
                self.discord.update_rich_presence(
                    text="Entering Giveaways",
                    show_entry=True, counter={"current": giveaway_counter, "max": len(self.valid_links)})
                self.system_manager.set_title("Cipher - Version " + self.system_manager.get_version(
                ) + "          |          Entering giveaway " + str(giveaway_counter) + " of " + str(len(self.valid_links)))
            except:
                pass

            random.shuffle(accounts)

            for account in accounts:
                entries_counter += 1
                tags = []

                if "c" in link["Modes"].lower():
                    try:
                        comment = self.file_manager.load_random_comment()
                        link.update({'Comment': comment})
                    except:
                        Printer.print(
                            "[red]No comment files found! No comment will be used!", timestamp=True)

                Printer.print("[magenta]Link " + str(giveaway_counter) + " [white]| [cyan]" +
                              account.get_handle() + "[white] |[yellow] Preparing", timestamp=True, ending=True)

                time.sleep(random.uniform(float(self.system_manager.get_delay(
                ) - 2), float(self.system_manager.get_delay() + 2)))

                # Like the post
                if "l" in link['Modes'].lower():
                    ret = account.like_post(
                        id=link['TweetId'], name=link['AuthorName'], link=link['TweetLink'])
                    if ret == "SKIP":
                        continue
                    if ret:
                        Printer.print("[magenta]Link " + str(giveaway_counter) + " [white]| [cyan]" +
                                      account.get_handle() + "[white] | [green]Liked", timestamp=True, ending=True)
                    time.sleep(random.uniform(float(self.system_manager.get_delay(
                    ) - 2), float(self.system_manager.get_delay() + 2)))

                # Retweet the tweet
                if "r" in link['Modes'].lower():
                    ret = account.retweet_post(
                        id=link['TweetId'], name=link['AuthorName'], link=link['TweetLink'])
                    if ret == "SKIP":
                        continue
                    if ret:
                        Printer.print("[magenta]Link " + str(giveaway_counter) + " [white]| [cyan]" +
                                      account.get_handle() + "[white] | [green]Retweeted", timestamp=True, ending=True)
                    time.sleep(random.uniform(float(self.system_manager.get_delay(
                    ) - 2), float(self.system_manager.get_delay() + 2)))

                # Follow all other tags
                if "f" in link['Modes'].lower():

                    if account.follow_account(id=link['AuthorId'], name=link['AuthorName'], link=link['TweetLink']):
                        Printer.print("[magenta]Link " + str(giveaway_counter) + "[white] | [cyan]" + account.get_handle() +
                                      "[white] |[green] Followed @" + link['AuthorName'], timestamp=True, ending=True)

                    if 'MentionIds' in link:
                        for i in range(len(link['MentionIds'])):

                            if account.follow_account(id=link['MentionIds'][i], name=link['MentionNames'][i], link=link['TweetLink']):
                                Printer.print("[magenta]Link " + str(giveaway_counter) + "[white] | [cyan]" + account.get_handle() +
                                              "[white] |[green] Followed user @" + link['MentionNames'][i], timestamp=True, ending=True)

                            time.sleep(random.uniform(float(self.system_manager.get_delay(
                            ) - 2), float(self.system_manager.get_delay() + 2)))

                if 't' in link['Modes'].lower():
                    if len(accounts) <= link['Modes'].lower().count('t'):
                        Printer.print("[red]Failed to tag for a giveaway by @" + link['AuthorName'] + " - you tried to tag " + str(link['Modes'].lower(
                        ).count('t')) + " friends when you only had " + str(len(accounts) - 1) + " accounts available to tag!", timestamp=True)
                    else:
                        while len(tags) < link['Modes'].lower().count('t'):
                            totag = random.choice(accounts)
                            if any(totag.get_handle() in s for s in tags):
                                continue
                            elif totag.get_handle() == account.get_handle():
                                continue
                            else:
                                tags.append('@' + totag.get_handle())

                        if link['Comment'] != '':
                            tags.append(link['Comment'])

                        image_id = None
                        if link["Image"] != "" and link["Image"] != None:
                            image_id = account.upload_media(
                                self.system_manager.get_file_manager().load_random_image())

                        quote = None

                        if "q" in link['Modes'].lower():
                            quote = link['TweetLink']

                        if account.comment_post(id=link['TweetId'], name=link['AuthorName'], link=link['TweetLink'], comment=' '.join(tags), media=image_id, quote=quote):
                            if "q" in link['Modes'].lower():
                                Printer.print("[magenta]Link " + str(giveaway_counter) + " [white]| [cyan]" +
                                              account.get_handle() + "[white] | [green]Quoted and tagged " + ', '.join(tags), timestamp=True, ending=True)
                            else:
                                Printer.print("[magenta]Link " + str(giveaway_counter) + "[white] | [cyan]" + account.get_handle() +
                                              "[white] |[green] Tagged " + ', '.join(tags), timestamp=True, ending=True)
                        time.sleep(random.uniform(float(self.system_manager.get_delay(
                        ) - 2), float(self.system_manager.get_delay() + 2)))

                elif "q" in link['Modes'].lower():

                    comment = "👀"

                    if link['Comment'] != '':
                        comment = link['Comment']

                    if account.comment_post(id=link['TweetId'], name=link['AuthorName'], link=link['TweetLink'], comment=comment, media=None, quote=link['TweetLink']):
                        Printer.print("[magenta]Link " + str(giveaway_counter) + " [white]| [cyan]" +
                                      account.get_handle() + "[white] | [green]Quoted", timestamp=True, ending=True)
                    time.sleep(random.uniform(float(self.system_manager.get_delay(
                    ) - 2), float(self.system_manager.get_delay() + 2)))

                elif link['Comment'] != '':
                    image_id = None
                    if link["Image"] != "" and link["Image"] != None:
                        image_id = account.upload_media(
                            self.system_manager.get_file_manager().load_random_image())
                    if account.comment_post(id=link['TweetId'], name=link['AuthorName'], link=link['TweetLink'], comment=link["Comment"], media=image_id, quote=None):
                        Printer.print("[magenta]Link " + str(giveaway_counter) + " [white]| [cyan]" + account.get_handle() +
                                      "[white] | [green]Commented " + link["Comment"], timestamp=True, ending=True)
                    time.sleep(random.uniform(float(self.system_manager.get_delay(
                    ) - 2), float(self.system_manager.get_delay() + 2)))

                elif link["Image"] != "" and link["Image"] != None:
                    image_id = account.upload_media(
                        self.system_manager.get_file_manager().load_random_image())
                    if account.comment_post(id=link['TweetId'], name=link['AuthorName'], link=link['TweetLink'], comment="", media=image_id, quote=None):
                        Printer.print("[magenta]Link " + str(giveaway_counter) + " [white]| [cyan]" + account.get_handle() +
                                      "[white] | [green]Posted an image", timestamp=True, ending=True)
                    time.sleep(random.uniform(float(self.system_manager.get_delay(
                    ) - 2), float(self.system_manager.get_delay() + 2)))
                Printer.print(
                    "                                                                                                    ", ending=True)

                data = {
                    "userid": str(self.system_manager.get_user_id()),
                    "account": "@" + account.get_handle(),
                    "link": link["TweetLink"],
                    "modes": link["Modes"],
                    "date": f'{datetime.datetime.now().strftime("%H:%M - %B %d, %Y")}'
                }

                try:
                    requests.post(
                        f"CIPHERWATCH_ENTRIES_API", json=data, timeout=5)
                except:
                    pass

            Printer.print("[magenta]Link " + str(giveaway_counter) +
                          " [white]|[green] Done", timestamp=True)
        Printer.print_line_center()
        Printer.print("[green]" + str(giveaway_counter) + " giveaways entered, for a total of " +
                      str(entries_counter) + " entries!", timestamp=True)

        try:
            newHeaders = {
                'Authorization': 'BEARER'
            }
            requests.post(f"ENTRIES_API",
                          params={"entries": int(entries_counter)}, headers=newHeaders)
        except:
            pass

    def collect_data(self):
        cont = False
        self.valid_links.clear()

        # SORT OUT BAD LINKS
        while True:

            Printer.print(
                '[magenta]What would you like to do?', timestamp=True)
            Printer.print('[white]1) Fetch links from #links', timestamp=True)
            Printer.print('[white]2) Use your own links.txt file',
                          timestamp=True)
            Printer.print('[magenta]X[white]) Go back', timestamp=True)
            inpt = Printer.input('[white]> ', timestamp=True)

            if inpt == '1':
                while True:
                    Printer.print_line_center()
                    Printer.print(
                        '[magenta]How many links would you like to fetch?', timestamp=True)
                    Printer.print('[magenta]X[white]) Go back', timestamp=True)
                    inpt2 = Printer.input('[white]> ', timestamp=True)

                    if inpt2.lower() == 'x':
                        self.collect_data()
                        break
                    try:
                        if int(inpt2) <= 75 and int(inpt2) > 0:
                            r = requests.get(
                                'LINK_API?amount=' + inpt2)
                            link_data = json.loads(r.text)['links']
                            cont = True
                            break
                        else:
                            Printer.print(
                                "[red]Invalid Input. Please input a number of links to fetch between 1 and 75", timestamp=True)
                    except:
                        Printer.print(
                            "[red]Invalid Input. Please input a number!", timestamp=True)
                break

            elif inpt == '2':
                try:
                    link_data = self.file_manager.load_links()
                    cont = True
                    break
                except:
                    Printer.print_error("FE03", "Could not read links.txt!")
                    self.system_manager.kill_system()

            elif inpt.lower() == 'x':
                self.system_manager.get_menu_handler().main_menu()
                break

            else:
                Printer.print(
                    "[red]Invalid Input. Please input 1-... or X", timestamp=True)

        Printer.print_line_center()
        # GET GOOD LINKS AND REMOVE DOUBLE LINKS
        if cont:
            Printer.print("[yellow]Giveaways are being checked...",
                          timestamp=True, ending=True)

            link_counter = 0
            for rawlink in link_data:
                link_counter += 1
                valid_link = {}
                mentionNames = []
                mentionIds = []

                try:
                    link = rawlink.split(("-"))[0]
                    if rawlink.count("-") == 2:
                        valid_link.update({'Modes': rawlink.split("-")[1]})
                        valid_link.update({'Comment': rawlink.split("-")[2]})
                    else:
                        valid_link.update({'Modes': rawlink.split("-")[1]})
                        valid_link.update({'Comment': ''})
                except:
                    Printer.print("[red]The link " + rawlink +
                                  " could not be read.", timestamp=True)
                    valid_link = {}
                    continue

                TweetId = link.split('/')[-1]

                try:
                    status = self.tweepy_client.get_tweet(
                        TweetId, expansions=["entities.mentions.username", "author_id"])

                    users = []
                    user_names = []

                    for user in status.includes['users']:
                        users.append(str(user["id"]))
                        user_names.append(user["name"])

                    author_id_str = str(users[0])
                    author_name = str(user_names[0])

                    users.pop(0)
                    user_names.pop(0)

                    foundCipher = False
                    for mention in user_names:
                        mentionNames.append(mention)
                    for mention in users:
                        if mention == "1288614902849048576":
                            foundCipher = True
                        mentionIds.append(mention)
                    valid_link.update({'MentionNames': mentionNames})
                    valid_link.update({'MentionIds': mentionIds})

                    if author_id_str == "1288614902849048576" or foundCipher:
                        continue

                    if "i" in rawlink.split("-")[1].lower():
                        valid_link.update({'Image': True})
                    else:
                        valid_link.update({'Image': None})

                    valid_link.update({'AuthorName': author_name})
                    valid_link.update({'AuthorId': author_id_str})
                    valid_link.update({'TweetId': TweetId})
                    valid_link.update({'TweetLink': link})
                    self.valid_links.append(valid_link)

                    Printer.print(
                        "                                                        ", ending=True)
                    Printer.print("[green]A link by @" + valid_link['AuthorName'] +
                                  " was checked successfully!        ", timestamp=True, ending=True)
                except Exception as e:
                    Printer.print(
                        "                                                                        ", ending=True)
                    Printer.print(
                        "[red]There was an error with a giveaway, and it was removed!", timestamp=True)
                    Printer.print("Error: " + str(e), timestamp=True)

            Printer.print(
                "                                                                        ", ending=True)
            Printer.print(
                "[green]All giveaways checked successfully!", timestamp=True, ending=True)
            Printer.print("")

    def check_proxies(self):

        accs = []
        proxy_arr = []

        try:
            raw_accs, groups = self.file_manager.read_accounts()
            for account in raw_accs:
                if not (account["Proxy"] == None or account["Proxy"] == ''):
                    if account["Proxy"] not in proxy_arr:
                        proxy_arr.append(account["Proxy"])
                        try:
                            try:
                                host, port, user, password = account["Proxy"] .split(
                                    ":")
                            except:
                                host, port = account["Proxy"] .split(":")
                        except:
                            Printer.print_error(
                                "FM03", "One of your proxies is corrupted!")
                            continue
                        try:
                            try:
                                account['WriteProxy'] = account["Proxy"]
                                account.update({
                                    'Proxy': {
                                        'http': 'http://' + f"{user}:{password}@{host}:{port}",
                                        'https': 'http://' + f"{user}:{password}@{host}:{port}"
                                    }
                                })
                                accs.append(account)
                            except:
                                account['WriteProxy'] = account["Proxy"]
                                account.update({
                                    'Proxy': {
                                        'http': 'http://' + f"{host}:{port}",
                                        'https': 'http://' + f"{host}:{port}"
                                    }
                                })
                                accs.append(account)
                        except:
                            Printer.print_error(
                                "FM04", "One of your proxies is corrupted!")
                            continue
        except Exception as e:
            Printer.print_error("FM02", "Could not read your accounts.csv!")
            self.system_manager.kill_system()

        table = []

        for acc in accs:
            table.append([acc["Proxy"]["http"].split(":")[2].split("@")[1], acc["Proxy"]["http"].split(":")[3], acc["Proxy"]
                         ["http"].split(":")[1].split("//")[1], acc["Proxy"]["http"].split(":")[2].split("@")[0], "", ""])

        Printer.print_table(table)

        for item in table:
            try:
                proxy = {
                    'http': 'http://' + f"{item[2]}:{item[3]}@{item[0]}:{item[1]}",
                    'https': 'http://' + f"{item[2]}:{item[3]}@{item[0]}:{item[1]}"
                }

                headers = Headers(
                    browser="chrome",
                    os="win",
                    headers=True
                ).generate()

                res = requests.get("https://www.twitter.com",
                                   headers=headers, proxies=proxy)

                if (res.status_code == 200):
                    item[4] = Printer.get_color(
                        "green") + "OK" + Printer.get_color("reset")
                else:
                    item[4] = Printer.get_color(
                        "red") + "FAILED" + Printer.get_color("reset")

                item[5] = str(round(res.elapsed.microseconds/1000)) + " ms"
            except:
                item[4] = Printer.get_color(
                    "red") + "FAILED" + Printer.get_color("reset")

            Printer.print_table(table)

        Printer.input('[green]Press enter when done >>>  ', timestamp=True)
