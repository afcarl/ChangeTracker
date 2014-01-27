import datetime

class Version():
    def __init__(self, text, comments, date, author):
        self.text = text
        self.comments = comments
        self.date = date
        self.author = author

    def showDate(self):
        return datetime.datetime.strptime(self.date, "%y%m%d%H%M")


    def __str__(self):
        return 'Author: '+ self.author + '\nDate: ' + str(self.showDate()) + '\nLength: ' + str(len(self.text))\
               + ' paragraphs\nComments: ' + str(len(self.comments))

    def __repr__(self):
        return 'Version('+ str(self.showDate()) +')'

class Comment():
    def __init__(self, text, id, date, author):
        self.text = text
        self.id = id
        self.date = date
        self.author = author

    def showDate(self):
        #to do: parse the datetime (difficulties due to local times)
        return self.date

    def __str__(self):
        return  '#' + self.author + ';;' + str(self.showDate()) + ';;' + self.text