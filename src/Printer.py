import datetime, os, threading
from tabulate import tabulate
from colorama import Fore, Style, init
init()

class Printer:

    @staticmethod
    def get_color(color):
        if color == "green":
            return Fore.GREEN
        elif color == "red":
            return Fore.RED
        elif color == "reset":
            return Fore.RESET
        elif color == 'cyan':
            return Fore.CYAN
        elif color == 'white':
            return Fore.WHITE
        elif color == 'bright':
            return Style.BRIGHT
        elif color == 'yellow':
            return Fore.YELLOW

    @staticmethod
    def print(string, timestamp=False, ending=False):

        string = Printer.replace_colorama(string)

        if timestamp:
            string = " " + Fore.WHITE + Style.BRIGHT + datetime.datetime.now().strftime("%H:%M:%S") + Fore.CYAN + ' │ ' + string
        
        if ending:
          print(" " + string, end="\r")

        else:
          print(" " + string)
        
    @staticmethod
    def print_error(error_code, error_message):
        Printer.print('[red]──────────┼────────────────────────────────────────────────────────')
        Printer.print(" " + Fore.WHITE + Style.BRIGHT + datetime.datetime.now().strftime("%H:%M:%S") + f'[red] │                      Error #{error_code}                      ')
        Printer.print(" " + Fore.WHITE + Style.BRIGHT + datetime.datetime.now().strftime("%H:%M:%S") + '[red] │                                                       ')
        Printer.print(" " + Fore.WHITE + Style.BRIGHT + datetime.datetime.now().strftime("%H:%M:%S") + '[red] │' + int((55-len(error_message))/2)*' ' + error_message + int((55-len(error_message))/2)*' ')
        Printer.print(" " + Fore.WHITE + Style.BRIGHT + datetime.datetime.now().strftime("%H:%M:%S") + '[red] │                 Please contact support                ')
        Printer.print('[red]──────────┼────────────────────────────────────────────────────────')

    @staticmethod
    def input(string, timestamp = False) -> str:

        string = Printer.replace_colorama(string)

        if timestamp:
            res = input("  " + Fore.WHITE + Style.BRIGHT + datetime.datetime.now().strftime("%H:%M:%S") + Fore.CYAN + ' │ ' + string)
        else:
            res = input(" " + string)
        
        return res

    @staticmethod
    def print_table(table):
        os.system('cls')
        print("  " + Fore.CYAN  + """
                 ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ 
                ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗
                ██║     ██║██████╔╝███████║█████╗  ██████╔╝
                ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
                ╚██████╗██║██║     ██║  ██║███████╗██║  ██║
                 ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝""")
        print(" " + "──────────┬────────────────────────────────────────────────────────" + Fore.RESET)
        print("  " + tabulate(table, ["IP", "Port", "User", "Pass", "Status", "Speed"], tablefmt="pretty"))

    @staticmethod
    def print_logo():
        Printer.print("""[bright][cyan]
               ██████╗██╗██████╗ ██╗  ██╗███████╗██████╗ 
              ██╔════╝██║██╔══██╗██║  ██║██╔════╝██╔══██╗
              ██║     ██║██████╔╝███████║█████╗  ██████╔╝
              ██║     ██║██╔═══╝ ██╔══██║██╔══╝  ██╔══██╗
              ╚██████╗██║██║     ██║  ██║███████╗██║  ██║
               ╚═════╝╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝""")

    @staticmethod
    def print_line_upper():
        print(Fore.CYAN + Style.BRIGHT + " " + "──────────┬────────────────────────────────────────────────────────")

    @staticmethod
    def print_line_center():
        print(Fore.CYAN + Style.BRIGHT + " " + "──────────┼────────────────────────────────────────────────────────")

    @staticmethod
    def print_line_lower():
        print(Fore.CYAN + Style.BRIGHT + " " + "──────────┴────────────────────────────────────────────────────────")

    @staticmethod
    def replace_colorama(string):
        #replace colors in string with colorama colors
        string = string.replace("[red]", Fore.RED)
        string = string.replace("[green]", Fore.GREEN)
        string = string.replace("[yellow]", Fore.YELLOW)
        string = string.replace("[blue]", Fore.BLUE)
        string = string.replace("[magenta]", Fore.MAGENTA)
        string = string.replace("[cyan]", Fore.CYAN)
        string = string.replace("[white]", Fore.WHITE)
        string = string.replace("[black]", Fore.BLACK)
        string = string.replace("[grey]", Fore.LIGHTBLACK_EX)
        string = string.replace("[lightgrey]", Fore.LIGHTBLACK_EX)
        string = string.replace("[lightred]", Fore.LIGHTRED_EX)
        string = string.replace("[lightgreen]", Fore.LIGHTGREEN_EX)
        string = string.replace("[lightyellow]", Fore.LIGHTYELLOW_EX)
        string = string.replace("[lightblue]", Fore.LIGHTBLUE_EX)
        string = string.replace("[lightmagenta]", Fore.LIGHTMAGENTA_EX)
        string = string.replace("[lightcyan]", Fore.LIGHTCYAN_EX)
        string = string.replace("[lightwhite]", Fore.LIGHTWHITE_EX)
        string = string.replace("[reset]", Style.RESET_ALL)
        #repalce bold colors with colorama bold
        string = string.replace("[bright]", Style.BRIGHT)
        string = string.replace("[nobold]", Style.NORMAL)

        return string