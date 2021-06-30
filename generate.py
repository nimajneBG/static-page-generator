#!/bin/python3

# Static Page generator
#
# (c) by Benjamin Grau 2021

from sys        import  exit, argv
from os         import  getcwd, path, listdir, mkdir
from colorama   import  Fore, Style, init
from markdown   import  Markdown
from json       import  loads
import                  shutil


# GENERAL TASKS:
#
# TODO: Implement syntax highlighting for code with prismjs 
# (CDN: https://www.jsdelivr.com/package/npm/prismjs)
# 
# TODO: Create an option to listen on changes in the source folder 
# and automatically recompile
#
# TODO: Make an option to create an nav / link list with all the top level pages


def error(msg: str, kill:bool=False) -> None:
    print(Fore.RED + Style.BRIGHT + 'ERROR: ' + Style.RESET_ALL + Fore.RED + msg + Style.RESET_ALL)
    if kill:
        exit()


class Generator():
    """"""

    def __init__(self):
        # Init variables
        self.CWD = getcwd()
        self.SRC_PATH = path.join(self.CWD, 'src')
        self.OUT_PATH = path.join(self.CWD, 'dest')
        self.ASSET_PATH = path.join(path.dirname(__file__), 'assets')
        self.TEMPLATE = ''
        self.mdExtentions = ['meta']

        # Read config files
        self.readConfig()
        self.readTemplate()

        # Init markdown parser
        self.md = Markdown(extensions = self.mdExtentions)

        # Init colorful output
        init()

    def readConfig(self) -> None:
        """Load the config from config.json"""
        CONFIG_PATH = path.join(self.CWD, 'config.json')
        if path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                config = f.read()
            self.CONFIG = loads(config)
        else:
            error('config.json not found')

    def readTemplate(self) -> None:
        """Load either a custom or the fallback template"""
        TEMPLATE_PATH = path.join(self.SRC_PATH, 'template.html')
        if path.isfile(TEMPLATE_PATH):
            with open(TEMPLATE_PATH) as f:
                self.TEMPLATE = f.read()

        # Use the basic fallback file instead
        else:
            TEMPLATE_PATH_FALLBACK = path.join(self.ASSET_PATH, 'template.fallback.html')
            if (path.isfile(TEMPLATE_PATH_FALLBACK)):
                with open(TEMPLATE_PATH_FALLBACK) as f:
                    self.TEMPLATE = f.read()
            else:
                error('template.html and fallback file not found')

    def findFiles(self) -> None:
        """Find all the Markdown files in the source directory"""
        files = []
        for i in listdir(self.SRC_PATH):
            if path.isfile(path.join(self.SRC_PATH, i)):
                if i.endswith('.md'):
                    files.append(i)
            else:
                # TODO: Implement finding non top level files/pages create 
                pass

        self.FILES = files

    def readFile(self, filename: str) -> dict:
        """Read files and """
        with open(filename) as f:
            mdIn = f.read()

        html = self.md.convert(mdIn)

        # Get the meta data (author, title etc.) from the last conversion
        # Although some IDEs say this line is an error it works and is 
        # right according to the documentation
        meta = self.md.Meta 

        # Create a easily usable dict with the meta data and the converted HTML
        data = dict()
        for key in meta.keys():
            data[key] = meta[key][0]
        data['html'] = html

        return data

    def copyStaticFiles(self) -> None:
        """Copy the static file folder"""
        if 'static-folder' in self.CONFIG and type(self.CONFIG['static-folder']) == str:
            STATIC_FOLDER_PATH = path.join(
                self.CWD, 
                self.OUT_PATH, 
                self.CONFIG['static-folder']
            )

            if path.isdir(STATIC_FOLDER_PATH):
                # Only do something if there are files/folders in the folder
                if len(listdir(STATIC_FOLDER_PATH)):
                    pass
            else:
                # HACK: For some reason directly using the CONFIG variable 
                # doesn't work, because of the []. So the folder name has to 
                # get his own variable
                FOLDER_NAME = self.CONFIG['static-folder']
                error(f'Static file folder ({FOLDER_NAME}) does not exist')

    def templatize(self, conntent: dict) -> str:
        """"""
        template = self.TEMPLATE
        template = template.replace('<!--TITLE-->',     conntent['title'])
        template = template.replace('<!--CONTENT-->',   conntent['html'])
        return template

    def getOutFilename(self, filename: str) -> str:
        """"""
        filename = path.join(self.OUT_PATH, filename)
        # All the files are of the type Markdown (found by fileextention),
        # so the fileextention will always be .md what is 3 characters long
        return f'{filename[0:-3]}.html'

    def saveFile(self, filename: str, conntent: str) -> None:
        """Write file"""
        with open(filename, 'w') as f:
            f.write(conntent)

    def processFile(self, filename: str) -> None:
        """Run alle the functions needed to convert one file (read, convert & save)"""
        contentMD = self.readFile(path.join(self.SRC_PATH, filename))
        contentHTML = self.templatize(contentMD)

        outFilename = self.getOutFilename(filename)

        self.saveFile(outFilename, contentHTML)
        print(f'📝 {filename}')

    def generate(self):
        """Run all the functions in the right order"""
        self.findFiles()
        for file in self.FILES:
            self.processFile(file)

        self.copyStaticFiles()
    


# Run the real main function 
if __name__ == "__main__":
    generator = Generator()
    generator.generate()
