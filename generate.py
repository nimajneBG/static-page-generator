#!/bin/python3
import sys
import markdown
import argparse
import os

class Generator():

    def __init__(self):
        self.CWD = os.getcwd()

    def checkArgs(self):
        parser = argparse.ArgumentParser(description='Create a static website from Markdown or HTML files.')
        parser.add_argument('inputfolder', type=str, help='Folder with the files the website should be created from')
        parser.add_argument('-o', '--outputfolder', type=str, help='Folder where the finished website should be dropped')
        parser.add_argument('--debug', type=bool, help='Prints debug info')
        self.args = parser.parse_args()
        
        # Check if the inputfolder exists
        if not os.path.exists(self.args.inputfolder):
            print("Inputfolder doesn't exists")
            sys.exit(2)

    def findFiles(self):
        print(os.listdir(os.path.join(self.CWD, self.args.inputfolder)))

    def generate(self):
        self.checkArgs()
        self.findFiles()


if __name__ == "__main__":
    generator = Generator()
    generator.generate()