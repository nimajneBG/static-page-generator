#!/bin/python3
import sys
import markdown
import argparse
import os

class Generator():

    def __init__(self):
        self.CWD = os.getcwd()

    def debug(self, text: str):
        if self.args.debug:
            print(text)

    def checkArgs(self):
        # Create a argparser
        parser = argparse.ArgumentParser(description='Create a static website from Markdown or HTML files.')

        # Create the arguments
        parser.add_argument('inputfolder', type=str, help='Folder with the files the website should be created from')
        parser.add_argument('outputfolder', type=str, help='Folder where the finished website should be dropped')
        parser.add_argument('-s', '--stylesheet', type=str, help='Stylesheet that should be used for the page')
        parser.add_argument('--markdown', type=bool, help='Pages are getting converted from Markdown to HTML before assembly')
        parser.add_argument('--debug', type=bool, help='Prints debug info')

        # Parse the args
        self.args = parser.parse_args()
        
        # Check if the inputfolder exists
        if not os.path.exists(self.args.inputfolder):
            print("Inputfolder doesn't exists")
            sys.exit(2)
        
        # Check if the outputfolder exists
        if not os.path.exists(self.args.outputfolder):
            print("Outputfolder doesn't exists")
            sys.exit(2)
        
        self.debug('Args checked')
        

    def findFiles(self):
        self.FILES = [i if os.path.isfile(os.path.join(self.CWD, self.args.inputfolder, i)) else [i, os.listdir(os.path.join(self.CWD, self.args.inputfolder, i))] for i in os.listdir(os.path.join(self.CWD, self.args.inputfolder))]
        self.debug(f'Files: {self.FILES}')

    def loadHeaderAndFooter(self):
        # Open <header>
        with open(os.path.join(self.CWD, self.args.inputfolder, '_header.html')) as f:
            self.HEADER = f.read()
        
        # Open <footer>
        with open(os.path.join(self.CWD, self.args.inputfolder, '_footer.html')) as f:
            self.FOOTER = f.read()
    
    def createHead(self):
        # Read the basic <head> from file
        with open(os.path.join(self.CWD, self.args.inputfolder, '_head.html')) as f:
            BASIC_HEAD = f.read()
        
        # Stylesheet
        if self.args.stylesheet != None:
            STYLESHEET = f'<link rel="stylesheet" href="{self.args.stylesheet}">'
        
        # Assembly
        self.HEAD = f'{BASIC_HEAD}{STYLESHEET}'

    def createNav(self):
        nav = ''

        # Specify the fileextention (either *.md or *.html)
        FILE_EXTENTION = 'md' if self.args.markdown else 'html'

        # Loop thro all files in the list
        for item in self.FILES:
            # A page
            if type(item) == str and item != '_header.html' and item != '_footer.html' and FILE_EXTENTION == item[-len(FILE_EXTENTION):]:
                title = item[:-(len(FILE_EXTENTION) + 1)] if item != f'index.{FILE_EXTENTION}' else 'Home'
                nav += f'<a class="nav_link" href="{item}">{title}</a>'
            # A sub-directory
            elif type(item) == list and f'index.{FILE_EXTENTION}' in item[1]:
                nav += f'<a class="nav_link" href="{item[0]}/index.{FILE_EXTENTION}">{item[0]}</a>'

        self.HEADER = self.HEADER.replace('<AutoNav />', nav)

    def generate(self):
        self.checkArgs()
        self.findFiles()
        self.createHead()
        self.loadHeaderAndFooter()
        self.createNav()
        for file in self.FILES:
            if type(file) == str and file != '_header.html' and file != '_footer.html':
                if self.args.markdown:
                    pass
                
            elif type(file) == list:
                pass
        self.debug(f'{self.HEADER}\n{self.FOOTER}')


if __name__ == "__main__":
    generator = Generator()
    generator.generate()