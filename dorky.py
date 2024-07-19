import argparse
import json
from rich.console import Console
from rich.table import Table
import pyperclip
import os

parser = argparse.ArgumentParser(prog='Dorky', description='Fast google dorks')
parser.add_argument('-s','-site', required=False, help='Set the site')
parser.add_argument('-p','-parameters', required=False, help="Set the wordlist containing the paramaters to look for")
parser.add_argument('-cp','-clipboard', default=False, action='store_true',help='Copy directly to clipboard')
parser.add_argument('-l','-list', required=False, action='store_true', help='List the saved wordlists')
parser.add_argument('-aw','-add-wordlist', required=False, help='Add a wordlist <name:/path/to/wordlist>')

args = parser.parse_args()

wordlists = {}
params_list = []
SITE = None
SELECTED_WORDLIST = None

if args.aw:
    name, path = args.aw.split(':')
    wordlists[name] = path

    with open('wordlists.json', 'w') as w_file:
        json.dump(wordlists, w_file)

    exit()

with open('wordlists.json', 'r') as w_file:
    wordlists = json.load(w_file)

    if not wordlists :
        print("No wordlists found use -aw name:/path/to/wordlist to save one")

if args.s:
    SITE = args.s

if args.p:
    if wordlists[args.p]:
        SELECTED_WORDLIST = wordlists[args.p]
    else:
        print("Please select a correct wordlist, use -l for help")


if args.l:
    t = Table(title= "Wordlists")
    t.add_column("Name")
    t.add_column("Path")

    for name, path in wordlists.items():
        t.add_row(name, path)

    c = Console()
    c.print(t)
    exit()

def dork_string(site, wordlist):

    DORK = f'site:{site} '

    with open(wordlist, 'r') as file:
        inurl_list = [line.strip() for line in file]

    for line in inurl_list:
        DORK+= f'inurl:{line} | '

    DORK = DORK[:-2]

    return DORK


if __name__ == '__main__':
    dork_string = dork_string(SITE, SELECTED_WORDLIST)
    if args.cp:
        print("Dork copied to your clipboard!")
        pyperclip.copy(dork_string)
    else:
        columns, _ = os.get_terminal_size()
        print("\n \tHere's your dork! \n")

        print('-' * columns)
        print(dork_string)
        print('-' * columns)