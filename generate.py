#!/bin/python3

# Static Page generator
#
# NOTE: This file is *intended* to be run
#
# (c) by Benjamin Grau 2021

from sys        import  exit, argv
from os         import  getcwd, path, listdir, mkdir
from colorama   import  Fore, Style, init
from markdown   import  Markdown
from json       import  loads
import                  shutil
import                  logging

from config     import  Config


# GENERAL TASKS:
#
# TODO: Implement syntax highlighting for code with prismjs
#       (CDN: https://www.jsdelivr.com/package/npm/prismjs)
#
# TODO: Create an option to listen on changes in the source folder
#       and automatically recompile
#
# TODO: Make an option to create an nav / link list with all the top 
#       level pages
#
# TODO: Move all the config stuff into a own class & file
#
# TODO: Custom Exceptions (exceptions.py) and using exceptions more
#
# TODO: Write Unitests



# Regex for a CDN link:
# LANG = 'css'
# ^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.css$
# CDN_REGEX = r'^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.css$'



class Generator():
    """Generator class"""

    # Init variables
    TEMPLATE = ''
    CWD = getcwd()
    ASSET_PATH = path.join(path.dirname(__file__), 'assets')

    SRC_PATH = path.join(CWD, 'src')
    DEST_PATH = path.join(CWD, 'dest')

    # Builtin extentions of the markdown converter
    # - `meta` is needed for getting the meta data from the file
    # - `extra` contains many diffrent extentions for images or tables
    #   for the behavior you would expect of markdown
    mdExtentions = ['meta', 'extra']

    def __init__(self, configFileName:str='config.json'):
        config = Config(configFileName, self.CWD)
        print(config.CONFIG_PATH)

        # Read config files
        self.readConfig()
        self.processConfig()
        self.readTemplate()

        # Init markdown parser
        self.md = Markdown(extensions = self.mdExtentions)

        # Init colorful output
        init()

    def error(self, msg: str, kill: bool=False) -> None:
        logging.error(msg)
        if kill:
            exit()

    def printEmoji(self, emoji: str, alt: str) -> str:
        """Returns the emoji if they are enabled in the config and the 
        alternative text if emojis are disabled.

        If nothing is specified in the config the default is to use 
        the emoji"""
        if 'emoji' in self.CONFIG.keys():
            if isinstance(self.CONFIG['emoji'], bool) and self.CONFIG['emoji']:
                return emoji
            elif not isinstance(self.CONFIG['emoji'], bool):
                varType = type(self.CONFIG['emoji'])
                self.error(f'`emoji` is of type {varType} should be {bool}. Defaulting to using emojis')
                return emoji
            else:
                # Printing the alt in bold and all caps
                return Style.BRIGHT + alt.upper() + Style.RESET_ALL
        else:
            # If no value is set default to using emojis
            return emoji

    def readConfig(self) -> None:
        """Load the config from config.json"""
        CONFIG_PATH = path.join(self.CWD, 'config.json')
        if path.isfile(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                config = f.read()
            self.CONFIG: dict = loads(config)
        else:
            self.error('config.json not found', True)

    def processConfig(self):
        """Process the contents of the config file"""

        configKeys = self.CONFIG.keys()

        # Get the path of the source directory
        if 'src-folder' in configKeys:
            # heck if it's the right type
            if isinstance(self.CONFIG['src-folder'], str):
                if path.isabs(self.CONFIG['src-folder']):
                    # Abstract path
                    pass
                else:
                    # Foldername
                    pass
            else:
                indexType = type(self.CONFIG['src-folder'])
                self.error(
                    f'Type of the config index `src-folder` is not a string ({indexType})',
                    True
                )
        else:
            # Default to `src` in the current working directory
            self.SRC_PATH = path.join(self.CWD, 'src')
            logging.info(f'Defaulting the SRC_PATH to {self.SRC_PATH}')

            # Check it exists
            if not path.isdir(self.SRC_PATH):
                raise FileNotFoundError(
                    f'''Defaulted the SRC_PATH to {self.SRC_PATH} which doesn't exist.
                    
                    Specify your source folder in the config file with `src-folder`'''
                )


        self.OUT_PATH = path.join(self.CWD, 'dest')


    def readTemplate(self) -> None:
        """Load either a custom or the fallback template"""
        TEMPLATE_PATH = path.join(self.SRC_PATH, 'template.html')
        if path.isfile(TEMPLATE_PATH):
            with open(TEMPLATE_PATH) as f:
                self.TEMPLATE = f.read()

        # Use the basic fallback file instead
        else:
            TEMPLATE_PATH_FALLBACK = path.join(
                self.ASSET_PATH,
                'template.fallback.html'
            )
            if (path.isfile(TEMPLATE_PATH_FALLBACK)):
                with open(TEMPLATE_PATH_FALLBACK) as f:
                    self.TEMPLATE = f.read()
            else:
                raise FileNotFoundError('template.html and fallback file not found')

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

        # Create a easily usable dict with the meta data and the 
        # converted HTML
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
                # HACK: For some reason directly using the CONFIG 
                # variable doesn't work, because of the []. 
                # So the folder name has to get his own variable
                FOLDER_NAME = self.CONFIG['static-folder']
                self.error(f'Static file folder ({FOLDER_NAME}) does not exist', True)

    def replaceInTemplate(self, template: str, content: dict, index: str, name=False) -> str:
        """"""
        # TODO: Use Exceptions/Warnings for the errors
        placeholder = f'<!--{name if name else index.upper()}-->'
        KEYS = content.keys()
        if placeholder in template:
            if index in KEYS:
                template = template.replace(placeholder, content[index])
            else:
                self.error(f'No value for {index} although it\'s used in the template')
        else:
            # Waring for unused placeholder
            pass
        return template

    def templatize(self, conntent: dict) -> str:
        """Place the conntent in the template.

        Returns the filled in template"""
        template = self.TEMPLATE
        template = self.replaceInTemplate(template, conntent, 'title')
        template = self.replaceInTemplate(template, conntent, 'html', 'CONTENT')
        return template

    def getOutFilename(self, filename: str) -> str:
        """"""
        filename = path.join(self.OUT_PATH, filename)
        # All the files are of the type Markdown (because they are found 
        # by fileextention) so the fileextention will always be .md what 
        # is 3 characters long
        return f'{filename[0:-3]}.html'

    def saveFile(self, filename: str, conntent: str) -> None:
        """Write file"""
        with open(filename, 'w') as f:
            f.write(conntent)

    def processFile(self, filename: str) -> None:
        """Run alle the functions needed to convert one file 
        (read, convert & save)"""
        contentMD = self.readFile(path.join(self.SRC_PATH, filename))
        contentHTML = self.templatize(contentMD)

        outFilename = self.getOutFilename(filename)

        self.saveFile(outFilename, contentHTML)

        # Output 'WROTE' instead of 📝 if emojis are disabled
        wroteMessage = self.printEmoji('📝', 'WROTE')
        print(f'{wroteMessage} {filename}')

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
