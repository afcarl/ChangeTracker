'''
This is an altered version of the docx library for python by Mike MacCana
Copyright (c) 2009-2010 Mike MacCana
http://github.com/mikemaccana/python-docx
'''

import zipfile

from lxml import etree
from version import Comment

# The Word prefixes / namespace matches used in document.xml & core.xml for text.

nsprefix = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def opendocx(file):
    '''Open a docx file, return a document XML tree'''
    try:
        mydoc = zipfile.ZipFile(file)
        xmlcontent = mydoc.read('word/document.xml')
        document = etree.fromstring(xmlcontent)
        return document
    except:
        raise IOError

def getdocumenttext(document):
    '''Return the raw text of a document, as a list of paragraphs.'''
    paratextlist = []
    # Compile a list of all paragraph (p) elements
    paralist = []
    for element in document.iter():
        # Find p (paragraph) elements
        if element.tag == '{'+nsprefix+'}p':
            paralist.append(element)
    # Since a single sentence might be spread over multiple text elements,
    # iterate through each paragraph, appending all text (t) children to that
    # paragraphs text.
    for para in paralist:
        paratext = u''
        # Loop through each paragraph
        for element in para.iter():
            # Find t (text) elements
            if element.tag == '{'+nsprefix+'}t':
                if element.text:
                    paratext = paratext+element.text
            elif element.tag == '{'+nsprefix+'}tab':
                paratext = paratext + '\t'
        # Add our completed paragraph text to the list of paragraph text
        if not len(paratext) == 0:
            paratextlist.append(paratext)
    return paratextlist

'''
the following functions are not from the original docx code
'''

def opencomments(path):
    '''
    if it exists, it opens and returns the document containing comments
    '''
    try:
        mydoc = zipfile.ZipFile(path)
        xmlcontent = mydoc.read('word/comments.xml')
        document = etree.fromstring(xmlcontent)
        return document
    except:
        raise IOError

def getcomments(document):
    '''
    parses existent comments from the .docx
    '''
    comments = []
    if document is not None:
        # Compile a list of all paragraph (p) elements
        commentlist = []
        for element in document.iter():
            # Find p (paragraph) elements
            if element.tag == '{'+nsprefix+'}comment':
                commentlist.append(element)

        for para in commentlist:
            commentdate = para.get('{'+nsprefix+'}date')
            commentauthor = para.get('{'+nsprefix+'}author')
            commentid = para.get('{'+nsprefix+'}id')

            # Loop through each comment
            commenttext = u''
            for element in para.iter():
                if element.tag == '{'+nsprefix+'}t':
                    if element.text:
                        commenttext = commenttext+element.text
                elif element.tag == '{'+nsprefix+'}tab':
                    commenttext = commenttext + '\t'

            comments.append(Comment(commenttext, commentid, commentdate, commentauthor))

    return comments

def getdocumenttext_withcomments(document, comments):
    '''
    same logic as getdocumenttext but additionally parses comments
    '''
    #logic only changes if there are comments
    if comments is not None:
        commentlist = getcomments(comments)
        paratextlist = []
        # Compile a list of all paragraph (p) elements
        paralist = []
        for element in document.iter():
            # Find p (paragraph) elements
            if element.tag == '{'+nsprefix+'}p':
                paralist.append(element)
        # Since a single sentence might be spread over multiple text elements,
        # iterate through each paragraph, appending all text (t) children to that
        # paragraphs text.
        for para in paralist:
            paratext = u''
            # Loop through each paragraph
            for element in para.iter():
                #find comment beginnings
                if element.tag == '{'+nsprefix+'}commentRangeStart':
                    id = element.get('{'+nsprefix+'}id')
                    for comment in commentlist:
                        if comment.id == id:
                            paratextlist.append(str(comment))
                # Find t (text) elements
                if element.tag == '{'+nsprefix+'}t':
                    if element.text:
                        paratext = paratext+element.text
                elif element.tag == '{'+nsprefix+'}tab':
                    paratext = paratext + '\t'
            # Add our completed paragraph text to the list of paragraph text
            if not len(paratext) == 0:
                paratextlist.append(paratext)
        return paratextlist
    else:
        return getdocumenttext(document)



