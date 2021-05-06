#!/bin/python3
from sys import exit, argv
from os import getcwd, path, listdir
from colorama import Fore, Style, init
from markdown import Markdown
from json import loads
import shutil


def error(msg: str) -> None:
    print(Fore.RED + Style.BRIGHT + 'ERROR: ' + Style.RESET_ALL + Fore.RED + msg + Style.RESET_ALL)


class Generator():
    """"""

    def __init__(self):
        self.CWD = getcwd()
        self.SRC_PATH = path.join(self.CWD, 'src')
        self.OUT_PATH = path.join(self.CWD, 'dest')
        self.ASSET_PATH = path.join(path.dirname(__file__), 'assets')
        self.md = Markdown(extensions = ['meta'])
        self.TEMPLATE = ''
        self.readConfig()
        self.readTemplate()
        init()

    def readConfig(self) -> None:
        CONFIG_PATH = path.join(self.CWD, 'config.json')
        if path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                config = f.read()
            self.CONFIG = loads(config)
        else:
            error('config.json not found')
            exit()

    def readTemplate(self) -> None:
        TEMPLATE_PATH = path.join(self.SRC_PATH, 'template.html')
        if path.isfile(TEMPLATE_PATH):
            with open(TEMPLATE_PATH) as f:
                self.TEMPLATE = f.read()
        else:
            TEMPLATE_PATH_FALLBACK = path.join(self.ASSET_PATH, 'template.fallback.html')
            if (path.isfile(TEMPLATE_PATH_FALLBACK)):
                with open(TEMPLATE_PATH_FALLBACK) as f:
                    self.TEMPLATE = f.read()
            else:
                error('template.html and fallback file found')
                exit()

    def findFiles(self) -> None:
        files = []
        for i in listdir(self.SRC_PATH):
            if path.isfile(path.join(self.SRC_PATH, i)):
                if i.endswith('.md'):
                    files.append(i)
            else:
                pass

        self.FILES = files

    def readFile(self, filename: str) -> dict:
        with open(filename) as f:
            mdIn = f.read()

        html = self.md.convert(mdIn)
        meta = self.md.Meta
        for key in meta.keys():
            meta[key] = meta[key][0]
        meta['html'] = html
        return meta

    def templatize(self, conntent: dict) -> str:
        template = self.TEMPLATE.replace('<!--TITLE-->', conntent['title'])
        template = template.replace('<!--CONTENT-->', conntent['html'])
        return template

    def getOutFilename(self, filename: str) -> str:
        filename = path.join(self.OUT_PATH, filename)
        filename = filename[0:-3] + '.html'
        return filename

    def saveFile(self, filename: str, conntent: str) -> None:
        with open(filename, 'w') as f:
            f.write(conntent)

    def processFile(self, filename: str) -> None:
        contentMD = self.readFile(path.join(self.SRC_PATH, filename))
        contentHTML = self.templatize(contentMD)

        outFilename = self.getOutFilename(filename)

        self.saveFile(outFilename, contentHTML)
        print('📝 {}'.format(filename))

    """def createNav(self):
        nav = ''

        # Loop thro all files in the list
        for item in self.FILES:
            # A page
            if type(item) == str:
                title = item[:-(len(self.FILE_EXTENTION) + 1)] if item != f'index.{self.FILE_EXTENTION}' else 'Home'
                nav += f'<a class="nav_link" href="{item}">{title}</a>'
            # A sub-directory
            elif type(item) == list and f'index.{self.FILE_EXTENTION}' in item[1]:
                nav += f'<a class="nav_link" href="{item[0]}/index.{self.FILE_EXTENTION}">{item[0]}</a>'

        self.HEADER = self.HEADER.replace('<AutoNav />', nav)
        """

    def generate(self):
        """Run all the functions in the right order"""
        # self.checkArgs()
        self.findFiles()
        for file in self.FILES:
            self.processFile(file)


if __name__ == "__main__":
    generator = Generator()
    generator.generate()
