"""
This file creates a checker for all input parameters
"""

import os
class InputChecker():

    def __init__(self, args, config):

        #settings are stored here
        self.settings = {"paper": "", "dir": "", "name": "", "source": ""}
        self.args = args
        self.config = config



    def check_config(self):
        """
        checks the config data and sets the variables for the settings
        """
        check_paper, check_name, check_source, check_folder = self.what_to_check()

        if check_paper:
            #does the papers dict exist?
            if not 'papers' in self.config:
                print 'please ensure that your settings.conf has the variable "papers"'
                return False

            #is papers dict emty?
            elif self.config['papers'] is None:
                print 'please ensure that your settings.conf has no empty variables'
                return False

            #does the paper from the argument exist in the papers dict?
            elif self.args.paper not in self.config['papers'].keys() \
                and self.args.paper[:-5] not in self.config['papers'].keys():
                print 'The paper you want to track does not exist in the settings.conf file'
                return False

        #special case: if no paper is specified but only one is in the config file - track it.
        elif len(self.config['papers']) > 1:
            print 'Please specify the paper you are working on by either having only one entry' \
                  ' in the papers variable or using an argument'
            return False

        #check only if not overwritten in command line
        if check_name:
            #does the name variable exist in config?
            if not 'name' in self.config:
                print 'please ensure that your settings.conf has the variable "name"'
                return False

            #is the name variable empty?
            elif self.config['name'] is None:
                print 'please ensure that your settings.conf has no empty variables'
                return False

        #check only if not overwritten in command line
        if check_folder:
            #does the variable exist?
            if not 'folder_name' in self.config:
                print 'please ensure that your settings.conf has the variable "folder_name"'
                return False

            #is the variable empty?
            elif self.config['folder_name'] is None:
                print 'please ensure that your settings.conf has no empty variables'
                return False

        self.set_settings(check_paper, check_name, check_source, check_folder)

        #the following can only get checked with existent settings - otherwise too much redundancy

        #does the source folder exist?
        if not os.path.exists(self.settings["source"]):
            print 'Your source folder seems to be nonexistent'
            return False

        #does the document exist?
        elif not os.path.exists(os.path.join(self.settings["source"], self.settings["paper"] + '.docx')) \
            and not os.path.exists(os.path.join(self.settings["source"], self.settings["paper"])):
                print 'Please ensure that a .docx with your specified name exists'
                return False

        #print os.path.join(self.settings["source"], self.settings["paper"] + '.docx')

        return True


    def what_to_check(self):
        '''
        determines where the settings are coming from (config or commmand line argument)
        A False means that it has to check the config file
        A True means that it has to check the argument
        '''
        check_paper = True
        check_name = True
        check_source = True
        check_folder = True
        if self.args.paper is None:
            check_paper = False
        if self.args.name is None:
            check_name = False
        if self.args.source is None:
            check_source = False
        if self.args.folder is None:
            check_folder = False

        return (check_paper, check_name, check_source, check_folder)



    def set_settings(self, check_paper, check_name, check_source, check_folder):
        """
        sets all settings in the dict

        settings = {"paper": "", "dir": "", "name": "", "source": ""}
        """
        if check_paper:
            if ".docx" in self.args.paper:
                self.settings["paper"] = self.args.paper[:-5]
            else:
                self.settings["paper"] = self.args.paper

        #as checked earlier there can be only one entry in the dict at this point - take it.
        else:
             self.settings["paper"] = self.config['papers'].keys()[0]

        if check_name:
            self.settings["name"] = self.args.name
        else:
            self.settings["name"] = self.config["name"]

        if check_source:
            self.settings["source"] = self.args.source
        else:
            self.settings["source"] = self.config["papers"][self.settings["paper"]]

        if check_folder:
            self.settings["folder"] = self.args.folder
        else:
            self.settings["folder"] = self.config["folder_name"]