import pathlib
import csv
import subprocess
import os
import pandas
import winshell
import json
import time
import datetime
import random
import sys
from shutil import rmtree
from win32com.client import Dispatch
from Printer import Printer
from discord_webhook import DiscordWebhook
import tkinter as tk
from tkinter import filedialog
import base64


class FileManager:
    def __init__(self, system_manager):
        if getattr(sys, 'frozen', False):
            self.default_path = pathlib.Path(sys.executable).parent.resolve()
        elif __file__:
            self.default_path = pathlib.Path(__file__).parent.resolve()
        self.accounts_path = pathlib.Path(
            self.default_path, 'settings', 'Twitter', 'accounts.csv')
        self.links_path = pathlib.Path(
            self.default_path, 'settings', 'Twitter', 'links.txt')
        self.settings_path_old = pathlib.Path(
            self.default_path, 'settings', 'settings.txt')
        self.settings_path = pathlib.Path(
            self.default_path, 'settings', 'settings.json')
        self.dms_path = pathlib.Path(self.default_path, 'settings', 'dms.csv')
        self.mentions_path = pathlib.Path(
            self.default_path, 'settings', 'mentions.csv')
        self.comments_path = pathlib.Path(
            self.default_path, 'settings', 'Twitter', 'Comments')
        self.images_path = pathlib.Path(
            self.default_path, 'settings', 'Twitter', 'Images')
        self.data_path = pathlib.Path(
            self.default_path, 'settings', 'Twitter', 'data.json')
        self.system_manager = system_manager
        self.lastran = {}

    def get_lastran(self):
        return self.lastran

    def get_default_path(self):
        return self.default_path

    def read_accounts(self, group=""):

        accounts = []
        groups = []

        with open(self.accounts_path, 'r') as csvFile:
            csvReader = csv.DictReader(csvFile)
            for row in csvReader:
                if group == "":
                    accounts.append(row)
                    if not row["Group"] in groups:
                        groups.append(row["Group"])
                elif row["Group"].lower() in group.lower():
                    accounts.append(row)
                    if not row["Group"] in groups:
                        groups.append(row["Group"])

        return accounts, groups

    def update_account(self, account):
        try:
            Writing = []
            with open(self.accounts_path, 'r') as csvFile:
                csvReader = csv.DictReader(csvFile)
                for row in csvReader:
                    if row['Handle'] == account.get_handle():
                        toWrite = row.copy()
                        toWrite['Proxy'] = account.get_write_proxy()
                        toWrite['Token'] = account.get_token()
                        toWrite['Group'] = account.get_group()
                        toWrite['Login'] = account.get_login()
                        toWrite['Password'] = account.get_password()
                        toWrite['Handle'] = account.get_handle()
                        toWrite['Info'] = account.get_Info()
                    else:
                        toWrite = row.copy()
                    Writing.append(toWrite)
        except:
            Printer.print(
                f'[red]Error loading account data for @{account.get_handle()}!', timestamp=True)
        try:
            with open(self.accounts_path, 'w', newline='') as f:
                writer = csv.DictWriter(
                    f, fieldnames=Writing[0].keys())
                writer.writeheader()
                writer.writerows(Writing)
        except Exception as e:
            Printer.print(
                f'[red]Error saving account data for @{account.get_handle()}!', timestamp=True)

    def save_settings(self):
        try:
            settings_data = {'key': self.system_manager.get_key(), 'delay': self.system_manager.get_delay(), 'webhook': self.system_manager.get_webhook(
            ), 'err_webhook': self.system_manager.get_error_webhook(), '2capkey': self.system_manager.get_capkey(), 'minlikes': self.system_manager.get_minlikes()}
            settings_file = open(self.settings_path, "w")
            settings_file.write(json.dumps(settings_data))
            settings_file.close()
            self.system_manager.re_auth()
        except:
            Printer.print_error(
                "FE01: Your settings file could not be read! Please contact support")
            self.system_manager.kill_system(5)

    def update_settings(self):
        try:
            key, delay, webhook, error_webhook, capkey, minlikes = self.load_settings()
            self.system_manager.set_key(key)
            self.system_manager.set_delay(delay)
            self.system_manager.set_webhook(webhook)
            self.system_manager.set_error_webhook(error_webhook)
            self.system_manager.set_capkey(capkey)
            self.system_manager.set_minlikes(minlikes)
        except:
            Printer.print_error(
                "FE01: Your settings file could not be read! Please contact support")
            self.system_manager.kill_system(5)

    def load_settings(self):
        settings_data = {}
        try:
            settings_file = open(self.settings_path, "r")
            settings_data = json.load(settings_file)
            settings_file.close()
        except:
            try:
                key, delay, webhook, error_webhook, capkey, minlikes = self.load_settings_old()
                settings_data = {'key': key, 'delay': delay, 'webhook': webhook,
                                 'err_webhook': error_webhook, '2capkey': capkey, 'minlikes': minlikes}
                with open(self.settings_path, "w") as settings_file:
                    json.dump(settings_data, settings_file)
            except Exception as e:
                Printer.print(
                    '[red]Error converting settings!', timestamp=True)

        if not self.settings_path.is_file():
            try:
                key, delay, webhook, error_webhook, capkey, minlikes = self.load_settings_old()
                settings_data = {'key': key, 'delay': delay, 'webhook': webhook,
                                 'err_webhook': error_webhook, '2capkey': capkey, 'minlikes': minlikes}
                with open(self.settings_path, "w") as settings_file:
                    json.dump(settings_data, settings_file)
            except Exception as e:
                Printer.print(
                    '[red]Error converting settings!', timestamp=True)
        else:
            try:
                os.remove(self.settings_path_old)
            except Exception as e:
                Printer.print(
                    '[red]Error converting settings!', timestamp=True)

        try:
            key = settings_data['key']

            delay = int(settings_data['delay'])
            if delay < 2:
                Printer.print(
                    '[red]Your delay is to low, please increase it to 2 or higher!', timestamp=True)
                self.system_manager.kill_system()

            webhook = settings_data['webhook']
            capkey = settings_data['2capkey']
            error_webhook = settings_data['err_webhook']
            minlikes = settings_data['minlikes']

            return key, delay, webhook, error_webhook, capkey, minlikes
        except:
            Printer.print_error(
                'FE01', 'Your settings file could not be read!')
            self.system_manager.kill_system()

    def load_settings_old(self):
        try:
            settings_file = open(self.settings_path_old, "r")
            settings_data = settings_file.readlines()
            settings_file.close()
        except Exception as e:
            Printer.print_error(
                'FM01', 'Your settings file could not be opened!')
            self.system_manager.kill_system()

        try:
            key = settings_data[0].split('=')[1]
            key = key[:-1]

            delay = int(settings_data[1].split('=')[1])
            if delay < 2:
                Printer.print(
                    '[red]Your delay is to low, please increase it to 2 or higher!', timestamp=True)
                self.system_manager.kill_system()

            webhook = settings_data[2].split('=')[1].replace("\n", "")

            try:
                capkey = str(settings_data[4].split("=")[1])
            except:
                with open(self.settings_path_old, "a") as f:
                    f.write("\n2CaptchaKey=")
                    settings_data.append("2CaptchaKey=")
                capkey = ""

            try:
                if len(settings_data) < 5:
                    with open(self.settings_path_old, "a") as f:
                        f.write("\nMinLikes=3")
                        settings_data.append("MinLikes=3")
                    if len(settings_data) < 6:
                        settings_data.append("\n" + settings_data[4])
                        settings_data[4] = "\n" + settings_data[3]
                        settings_data[3] = "\nERR_WEBHOOK="
                        a_file = open(self.settings_path_old, "w")
                        a_file.writelines(settings_data)
                        a_file.close()

                    error_webhook = settings_data[3].split(
                        '=')[1].replace("\n", "")
                else:

                    if len(settings_data) < 6:
                        settings_data.append("" + settings_data[4])
                        settings_data[4] = "\n" + settings_data[3]
                        settings_data[3] = "ERR_WEBHOOK="
                        a_file = open(self.settings_path_old, "w")
                        a_file.writelines(settings_data)
                        a_file.close()

                    error_webhook = settings_data[3].split(
                        '=')[1].replace("\n", "")

                    minlikes = settings_data[5].split("=")[1]
                    if not minlikes.isdigit():
                        settings_data[5] = "MinLikes=3"
                        a_file = open(self.settings_path_old, "w")
                        a_file.writelines(settings_data)
                        a_file.close()
            except:
                settings_data[5] = "MinLikes=3"
                a_file = open(self.settings_path_old, "w")
                a_file.writelines(settings_data)
                a_file.close()

            return key, delay, webhook, error_webhook, capkey, minlikes
        except:
            Printer.print_error(
                'FE01', 'Your settings file could not be read!')
            self.system_manager.kill_system()

    def load_links(self):
        link_file = open(self.links_path, "r", encoding="utf8")
        link_data = link_file.readlines()
        link_file.close()
        return link_data

    def cleanup_mei(self):
        mei_bundle = getattr(sys, "_MEIPASS", False)

        if mei_bundle:
            dir_mei, current_mei = mei_bundle.split("_MEI")
            for file in os.listdir(dir_mei):
                if file.startswith("_MEI") and not file.endswith(current_mei):
                    try:
                        rmtree(os.path.join(dir_mei, file))
                    except PermissionError:  # mainly to allow simultaneous pyinstaller instances
                        pass

    def validate_structure(self):
        try:
            for file in os.listdir(self.default_path):
                if os.path.isfile(os.path.join(self.default_path, file)) and 'Cipher-' in file:
                    os.remove(file)
        except:
            pass

        if not os.path.exists(self.dms_path):
            with open(self.dms_path, "w+") as f:
                f.write("Account,Host,Content,Date\n")
        if not os.path.exists(self.mentions_path):
            with open(self.mentions_path, "w+") as f:
                f.write("Account,Host,Link,Content,Date\n")

        df = pandas.read_csv(self.accounts_path)
        if not "Info" in df.columns:
            df["Info"] = ""
            df.to_csv(self.accounts_path, index=False)

    def create_shortcut(self, exe):
        desktop = winshell.desktop()
        shortpath = os.path.join(desktop, "Cipher.lnk")
        target = str(self.default_path / exe)
        wdir = str(self.default_path)

        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortpath)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = wdir
        shortcut.IconLocation = target
        shortcut.save()

    def open_file(self, filename):
        if filename == 'settings':
            os.startfile(self.settings_path_old)
        elif filename == 'accounts':
            os.startfile(self.accounts_path)
        elif filename == 'links':
            os.startfile(self.links_path)
        elif filename == 'comments':
            try:
                os.startfile(self.comments_path)
            except:
                Printer.print("[red]There is no Comments folder to open!")
        elif filename == 'images':
            try:
                os.startfile(self.images_path)
            except:
                os.mkdir(self.images_path)
                os.startfile(self.images_path)

    def replace_key(self, new_key):
        settings_file = open(self.settings_path, "rt")
        settings_data = json.load(settings_file)
        settings_file.close()
        settings_data["key"] = new_key
        settings_file = open(self.settings_path, "wt")
        settings_file.write(json.dumps(settings_data))
        settings_file.close()

    def load_time(self):
        try:
            with open(self.data_path) as file:
                self.lastran = json.load(file)

            for group in self.system_manager.get_account_manager().get_groups():
                try:
                    if self.lastran[group]['timestamp'] == None or self.lastran[group]['time'] == None or self.lastran[group]['timestamp'] == 0 or self.lastran[group]['time'] == 0:
                        self.lastran[group]['timestamp'] = int(
                            round(time.time() * 1000))
                        self.lastran[group]['time'] = datetime.datetime.utcnow().strftime(
                            "%a %b %d %X %Y")
                        try:
                            with open(self.data_path, 'w') as file:
                                file.write(json.dumps(self.lastran, indent=4))
                        except:
                            pass
                except:
                    self.lastran[group] = {}
                    self.lastran[group]['timestamp'] = int(
                        round(time.time() * 1000))
                    self.lastran[group]['time'] = datetime.datetime.utcnow().strftime(
                        "%a %b %d %X %Y")
                    try:
                        with open(self.data_path, 'w') as file:
                            file.write(json.dumps(self.lastran, indent=4))
                    except:
                        pass

        except:
            Printer.print_error('FE04', 'Your data.json file is corrupt!')
            self.system_manager.kill_system(10)

    def update_time(self):
        for group in self.system_manager.get_account_manager().get_groups():
            try:
                self.lastran[group]['timestamp'] = int(
                    round(time.time() * 1000))
                self.lastran[group]['time'] = datetime.datetime.utcnow().strftime(
                    "%a %b %d %X %Y")
                with open(self.data_path, 'w') as file:
                    file.write(json.dumps(self.lastran, indent=4))
            except:
                Printer.print_error('FE04', 'Your data.json file is corrupt!')

    def load_random_comment(self):
        file_name = random.choice(os.listdir(self.comments_path))
        with open(self.comments_path / file_name, 'r') as f:
            return f.read()

    def load_random_image(self):
        file_name = random.choice(os.listdir(self.images_path))
        with open(self.images_path / file_name, "rb") as image_file:
            data = base64.b64encode(image_file.read())
        return data

    def write_mentions(self, write):
        with open(self.mentions_path, 'a', newline='') as csvfile:
            fieldnames = ['Account', 'Host', 'Link', 'Content', 'Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(write)

    def write_dms(self, write):
        with open(self.dms_path, 'a', newline='') as csvfile:
            fieldnames = ['Account', 'Host', 'Content', 'Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(write)

    def send_files_to_support(self):
        try:
            try:
                webhook = DiscordWebhook(url='SUPPORT_WEBHOOK',
                                         content='Files recieved from <@!' + str(self.system_manager.get_user_id()) + "> (" + self.system_manager.get_name() + ")")
            except:
                pass
            with open(self.settings_path, "rb") as f:
                webhook.add_file(file=f.read(), filename='settings.txt')
            with open(self.accounts_path, "rb") as f:
                webhook.add_file(file=f.read(), filename='accounts.csv')

            webhook.execute()
        except:
            Printer.print(
                "[red]Files Missing - Please contact us in your ticket!")

    def import_accounts(self):
        root = tk.Tk()
        root.withdraw()

        Printer.print_line_center()
        Printer.print(
            "[yellow]Please select your accounts file for import...", timestamp=True, ending=True)

        file_path = filedialog.askopenfilename(title="Account File", filetypes=[
                                               ("Account Files", "*.txt *.csv")])
        if file_path == None or file_path == "":
            Printer.print(
                "                                                                                       ", timestamp=True, ending=True)
            Printer.print("[red]No file selected. Aborting...", timestamp=True)
            time.sleep(2)
            return

        Printer.print(
            "                                                                                       ", timestamp=True, ending=True)
        Printer.print("[green]Received file!", timestamp=True)

        with open(file_path, 'r') as file:
            lines = file.readlines()

            if lines[0] == "Phone Number,Twitter Handle,Pasword,OAuth Login Token\n":
                Printer.print("[green]File matches Promethan provider file type! Detected [magenta]" +
                              str(len(lines)-1) + " [green]accounts to import...", timestamp=True)
                Printer.print(
                    "[yellow]Please enter a group name:", timestamp=True)
                group = Printer.input("[white]> ", timestamp=True)
                for line in lines:
                    if line != "Phone Number,Twitter Handle,Pasword,OAuth Login Token\n":
                        line = line.split(",")
                        handle = line[1]
                        Printer.print(
                            "                                                                                                                               ", timestamp=True, ending=True)
                        Printer.print("[green]Importing account [magenta]" +
                                      handle + "...", timestamp=True, ending=True)
                        password = line[2]
                        token = line[3].replace('\n', '')

                        accounts_file = open(self.accounts_path, 'r')
                        acc_lines = accounts_file.readlines()
                        accounts_file.close()

                        accounts_file = open(self.accounts_path, 'a')
                        if not "\n" in acc_lines[-1]:
                            accounts_file.write('\n{},{},{},{},{},,'.format(
                                group, handle, password, handle, token))
                        else:
                            accounts_file.write('{},{},{},{},{},,'.format(
                                group, handle, password, handle, token))
                        accounts_file.close()
                Printer.print(
                    "[green]All accounts have been imported successfully!", timestamp=True)
                time.sleep(2)

            elif "Username,Password,Phone,Oauth_Token\n" in lines[0]:
                Printer.print("[green]File matches TW-Shop provider file type! Detected [magenta]" +
                              str(len(lines)-1) + " [green]accounts to import...", timestamp=True)
                Printer.print(
                    "[yellow]Please enter a group name:", timestamp=True)
                group = Printer.input("[white]> ", timestamp=True)
                for line in lines:
                    if not "Username,Password,Phone,Oauth_Token\n" in line:
                        line = line.split(",")
                        handle = line[0]
                        Printer.print(
                            "                                                                                                                               ", timestamp=True, ending=True)
                        Printer.print("[green]Importing account [magenta]" +
                                      handle + "...", timestamp=True, ending=True)
                        password = line[1]
                        token = line[3].replace('\n', '')

                        accounts_file = open(self.accounts_path, 'r')
                        acc_lines = accounts_file.readlines()
                        accounts_file.close()

                        accounts_file = open(self.accounts_path, 'a')
                        if not "\n" in acc_lines[-1]:
                            accounts_file.write('\n{},{},{},{},{},,'.format(
                                group, handle, password, handle, token))
                        else:
                            accounts_file.write('{},{},{},{},{},,'.format(
                                group, handle, password, handle, token))
                        accounts_file.close()
                Printer.print(
                    "[green]All accounts have been imported successfully!", timestamp=True)
                time.sleep(2)
            else:
                print(lines[0].strip())
                Printer.print(
                    "[red]File does not match provider file type! Other types are not supported yet.", timestamp=True)
                time.sleep(3)
                return
