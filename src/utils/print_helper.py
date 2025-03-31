from colorama import Fore, Style, init
from typing import Literal

init(autoreset=True)

class PrintHelper:
    def __init__(self):
        self.colors = {
            'cyan': Fore.CYAN,
            'green': Fore.GREEN,
            'red': Fore.RED
        }

    def cyan_print(self, text):
        print(Fore.CYAN + text)

    def green_print(self, text):
        print(Fore.GREEN + text)

    def red_print(self, text):
        print(Fore.RED + text)

    def yellow_print(self, text):
        print(Fore.YELLOW + text)
        
    def line_print(self, color: Literal['cyan', 'green', 'red', None] = None):
        if color is None:
            print('\n----------------------------------------\n')
        else:
            print(self.colors[color] + '\n----------------------------------------\n')

print_helper = PrintHelper()