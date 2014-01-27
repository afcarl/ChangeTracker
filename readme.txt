Version 0.1
The current version can store the text of different versions of .docx files.
In order to use it please enter your information in the settings.conf.
To get more information about how to run it please enter 'python changetracker.py --help'

The program was only tested in windows. Please notify me about every error you encounter.


To Do:

work on the logic that compares the versions and determines conflicts
loader for the last n saves
parse comments directly from word


Information about the .docx format:
You can open a .docx file using 7zip, winrar or similar programs because underlying it is a .zip format. The important
files for parsing are in the word subfolder (namely the files comments.xml and document.xml). The library docx for
python can parse the document.xml file but not the comment..xml file. We need to write this!
Other maybe interesting files are docProps/app.xml and docProps/core.xml, both of which contain general information (last
edited, who created it etc.)


Research for logic:
https://tug.org/pracjourn/2007-3/henningsen/henningsen.pdf (version control, no AI)



Largest competitors / similar tools:
most of them are using a version control for collab. writing. None of them offer AI features
they are either stand alone or in the web. Noone offers the features using word.

http://www.mixedink.com/#/_unique_features
http://ets.tlt.psu.edu/wp-content/uploads/7things_collaborative_writing_0.pdf
https://editorially.com/ 
http://www.educatorstechnology.com/2013/05/5-excellent-web-tools-to-teach.html