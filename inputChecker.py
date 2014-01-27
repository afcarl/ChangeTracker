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
            if not 'papers' in self.config:
                print 'please ensure that your settings.conf has the variable "papers"'
                return False
            elif self.config['papers'] is None:
                print 'please ensure that your settings.conf has no empty variables'
                return False
            elif self.args.paper not in self.config['papers'].keys() \
                and self.args.paper[:-5] not in self.config['papers'].keys():
                print 'The paper you want to track does not exist in the settings.conf file'
                return False
        elif len(self.config['papers']) > 1:
            print 'Please specify the paper you are working on by either having only one entry' \
                  ' in the papers variable or using an argument'
            return False


        if check_name:
            if not 'name' in self.config:
                print 'please ensure that your settings.conf has the variable "name"'
                return False
            elif self.config['name'] is None:
                print 'please ensure that your settings.conf has no empty variables'
                return False

        if check_folder:
            if not 'folder_name' in self.config:
                print 'please ensure that your settings.conf has the variable "folder_name"'
                return False
            elif self.config['folder_name'] is None:
                print 'please ensure that your settings.conf has no empty variables'
                return False

        self.set_settings(check_paper, check_name, check_source, check_folder)


        if not os.path.exists(self.settings["source"]):
            print 'Your source folder seems to be nonexistent'
            return False
        elif not os.path.exists(self.settings["source"] + self.settings["paper"] + '.docx') \
            and not os.path.exists(self.settings["source"] + self.settings["paper"]):
                print 'Please ensure that a .docx with your specified name exists'
                return False


        return True


    def what_to_check(self):
        '''
        determines where the settings are coming from
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