import os, re

from os.path import join, dirname, realpath

import docx_parser
from lxml import etree
import zipfile
from  version import Comment


nsprefix = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


if __name__ == '__main__':
    #nu1 = open_version(r'D:\test\changetracker\test1\1401161507_gehrmans.txt')
    #print nu1
    '''
    doc = docx_parser.opendocx(r'D:\test\Test2.docx')
    com = docx_parser.opencomments(r'D:\test\Test2.docx')

    b = docx_parser.getdocumenttext_withcomments(doc, com)
    for a in b:
        print a

    '''
    try:
        a = int('123')
    except:
        print 'a'
    else:
        print 'b'
