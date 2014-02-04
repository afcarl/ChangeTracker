import argparse
import os

from fileLoader import FileLoader
from inputChecker import InputChecker
from os.path import dirname, join, realpath

#create parser
parser = argparse.ArgumentParser(description="Track changes in word documents")
parser.add_argument('paper', action="store", nargs="?", help = "enter the name of your paper you specified in the settings.conf")
parser.add_argument('-s', '--source', action="store", nargs="?", help = "enter the source folder of the paper if not already in settings")
parser.add_argument('-n', '--name', action="store", nargs="?", help = "enter your name if it differs from your settings.conf")
parser.add_argument('-f', '--folder', action="store", nargs="?", help = "enter the folder the changes should get stored in")
parser.add_argument('-c', '--config', action="store_true", help = "Opens the config file.")
args = parser.parse_args()


if args.config:
    try:
        os.system("start " + join(dirname(realpath(__file__)), "settings.conf"))

    except:
        print "please ensure you have a settings.conf file"
else:

    #read the config file
    config = {}
    execfile(join(dirname(realpath(__file__)), "settings.conf"), config)

    checker = InputChecker(args, config)

    if checker.check_config():
        print "start the logic! Everything seems to work"
        settings = checker.settings
        #load newest version
        loader = FileLoader(settings["folder"], settings["paper"], settings["source"], settings["name"])
        curr_text = loader.load_text(settings["paper"] + '.docx')
        #analyse here
        loader.save_file(curr_text)




