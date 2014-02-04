import codecs
import datetime
import os
import re

from docx_parser import opendocx, opencomments, getdocumenttext_withcomments
from version import Version
from os.path import basename, exists, join


class FileLoader():
    """
    Can load text and comments from docx documents, extract the paragraphs and store them in a new file.
    Desired usage is to store each version of a written paper in a directory and then evaluate them

    can also load different versions of previously stored changes
    """


    def __init__(self, app_name, paper_name, standard_dir, creator):
        self.app_name = app_name
        self.paper_name = paper_name
        self.standard_dir = standard_dir
        self.creator = creator


    def create_filename(self):
        '''
        creates the file name for a change track using the datetime and creator
        format is always DATE_CREATOR.txt
        '''
        curr_time = datetime.datetime.utcnow()
        time_string =  str(curr_time.strftime("%y%m%d%H%M"))
        filename = str(time_string) + "_" + self.creator + ".txt"
        return filename

    def save_file(self, paragraphs):
        '''
        stores the paragraphs containing the text
        changes for future: add the save of comments
        '''
        filename = self.create_filename()
        try:
            if not exists(join(self.standard_dir, self.app_name)):
                os.makedirs(join(self.standard_dir, self.app_name))
            if not exists(join(self.standard_dir, self.app_name, self.paper_name)):
                os.makedirs(join(self.standard_dir, self.app_name, self.paper_name))
        except:
            print "could not create folder for storing"
        try:
            newfile = open(join(self.standard_dir, self.app_name, self.paper_name, filename), 'w')
        except:
            print "Could not access " + join(self.standard_dir, self.app_name, self.paper_name, filename)
        newfile.write('\n'.join(paragraphs))

    def load_text(self, filename):
        '''
        extract the text from a word document
        '''
        newtextlist = []
        try:
            document = opendocx(join(self.standard_dir, filename))
        except:
            print "could not open document. Text list will be empty"
        else:
            try:
                comments = opencomments(join(self.standard_dir,  filename))
            except:
                comments = None
            try:
                textlist = getdocumenttext_withcomments(document, comments)
                for paratext in textlist:
                    newtextlist.append(paratext.encode("utf-8"))
            except:
                print "could not read the text in the document"
        return newtextlist

    def get_versions(self):
        '''
        loads all old versions
        '''
        dir = join(self.standard_dir, self.app_name, self.paper_name)
        files = []
        for (dirpath, dirnames, filenames) in os.walk(dir):
            files.extend(filenames)
        if not files:
            print 'There seems to be no old version for this paper. Please Check your configuration'
            print 'We are currently looking here: ', join(self.standard_dir, self.app_name, self.paper_name)

        version_names = []
        #use only the files with the right names (DATE_AUTHOR.txt)
        pattern = r"\d\d[01]\d[0123]\d[012]\d[012345]\d\_\w+\.txt"
        for filename in files:
            match =  re.match(pattern, filename)
            if match:
                version_names.append(filename)

        versions = []
        for v in version_names:
            versions.append(self.open_version(join(dir, v)))

        return versions


    def open_version(self, path):
        '''
        opens a version of a change track and creates the version object from it

        uses codecs to decode the utf-8, use of utf-8-sig because of a potential BOM
        '''
        with codecs.open(path, encoding="utf-8-sig") as f:
            comments = []
            paras = []
            for line in f:
                if line[0] == '#':
                    comments.append(line)
                else:
                    paras.append(line)

            file_name =  basename(path).split('.')[0].split('_')

            #gets the date and the name of the author from the file name
            return Version(paras, comments, file_name[0], file_name[1])



if __name__ == '__main__':
    #this is for testing, final version doesn't need the hardcoded thing
    TEST_CHECK = True
    TEST_NAME = "test1"
    TEST_DIR = "D:\\test\\"
    TEST_FILE = "Test2.docx"

    if TEST_CHECK == True:
        myLoader = FileLoader("changetracker", "Test2", TEST_DIR, "gehrmans")
        mytext = myLoader.load_text(TEST_FILE)
        myLoader.save_file(mytext)
        #a = myLoader.get_versions()

        #for version in a:
        #    print version







