'''
dblp.xml -> authors.txt
'''

import codecs
from xml.sax import handler, make_parser

paper_tag = (
    'article',
    'inproceedings',
    'proceedings',
    'book',
    'incollection',
    'phdthesis',
    'mastersthesis',
    'www'
)
keywords = ('attention', 'transformer')
specific_year = 2017
split_str = ' ||| '

class mHandler(handler.ContentHandler):
    def __init__(self,result):
        self.result = result
        self.flag_author = False
        self.flag_title = False
        self.flag_year = False
        self.work_info = {}

    def startElement(self, name, attrs):
        if name == 'year':
            self.flag_year = True
        if name == 'title':
            self.flag_title = True
        if name == 'author':
            self.flag_author = True

    def endElement(self, name):
        if name == 'year':
            self.flag_year = False
        if name == 'title':
            self.flag_title = False
        if name == 'author':
            self.flag_author = False

        if name in paper_tag:
            if self.work_info.get('year', 0) >= specific_year and \
                    (keywords[0] in self.work_info.get('title', '') or \
                    keywords[1] in self.work_info.get('title', '')):
                self.result.write(str(self.work_info['year'])+split_str)
                self.result.write(str(self.work_info['title'])+split_str)
                authors = self.work_info.get('author', tuple())
                for author in authors:
                    if len(author)>3 and author[-4] == '0':
                        author = author[:-5]
                    self.result.write(author+split_str)
                self.result.write('\r\n')

            self.work_info = {}
            self.flag_write = False
            self.flag_title = False
            self.flag_year = False

    def characters(self, content):
        if self.flag_year:
            self.work_info['year'] = int(content)
        if self.flag_title:
            self.work_info['title'] = str.lower(content)
        if self.flag_author:
            self.work_info['author'] = self.work_info.get('author', tuple()) + (str.lower(content),)


def parserDblpXml(source,result):
    handler = mHandler(result)
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.parse(source)


if __name__ == '__main__':
    xml_file_name = './dblp-2022-04-01.xml'
    # xml_file_name = './test.xml'
    source = codecs.open(xml_file_name, 'r', 'utf-8')
    result = codecs.open('./authors.txt', 'w', 'utf-8')
    parserDblpXml(source,result)
    result.close()
    source.close()

'''
python getAuthors.py
'''