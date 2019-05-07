#!/usr/bin/python

import re
import sqlite3
import itertools
import dataclasses

@dataclasses.dataclass
class Location:
    chapters: [int]
    verses: [int]
    
@dataclasses.dataclass
class Reference:
    name: str
    locations: [Location]

def flatten(l):
    flat_list = []
    _ = [flat_list.extend(item) if isinstance(item, list) else flat_list.append(item) for item in l if item]
    return flat_list
    
class Parser:
    VERSES_LOCATION_PATTERN = (
        r"(?P<Chapter>1?[0-9]?[0-9])" +
        r"(-(?P<ChapterEnd>\d+)|,\s*(?P<ChapterNext>\d+))*" +
        r"(:\s*(?P<Verse>\d+))?" +
        r"(-(?P<VerseEnd>\d+)|,\s*(?P<VerseNext>\d+))*"
    )
    BIBLE_REFERENCE_PATTERN = (
        r"(?P<Book>(([1234]|I{1,4})[\t\f\r\n\v ]*)?\w+)\.?[\t\f\r\n\v ]+" +
        r"(?P<Locations>(" + VERSES_LOCATION_PATTERN + r"\s?)+)"
    )
    
    re_loc = re.compile(VERSES_LOCATION_PATTERN)
    re_ref = re.compile(BIBLE_REFERENCE_PATTERN, re.M)
    
    @staticmethod
    def matches(string):
        m = [m.groupdict() for m in Parser.re_ref.finditer(string)]
        refs = []
        for d in m:
            l = [l.groupdict() for l in Parser.re_loc.finditer(d['Locations'])]
            locations = []
            for loc in l:
                try:
                    chVal = int(loc['Chapter'])
                    chapters = [chVal]
                    if loc['ChapterEnd'] != None:
                        chEnd = int(loc['ChapterEnd'])
                        chapters.append(list(range(chVal + 1, chEnd)))
                    if loc['ChapterNext'] != None:
                        chNext = int(loc['ChapterNext'])
                        chapters.append(chNext)
                    verses = []
                    if loc['Verse'] != None:
                        vrVal = int(loc['Verse'])
                        verses = [vrVal]
                        if loc['VerseNext'] != None and loc['VerseEnd'] != None:
                            vrNext = int(loc['VerseNext'])
                            vrEnd = int(loc['VerseEnd'])
                            verses.append(list(range(vrNext, vrEnd)))
                        else:
                            if loc['VerseEnd'] != None:
                                vrEnd = int(loc['VerseEnd'])
                                verses.append(list(range(vrVal + 1, vrEnd)))
                            if loc['VerseNext'] != None:
                                vrNext = int(loc['VerseNext'])
                                verses.append(vrNext)
                    locations.append(Location(flatten(chapters), flatten(verses)))
                except Exception as e:
                    raise NameError('No chapter found')
            refs.append(Reference(d['Book'], locations))
        return refs
            
class BookMap:
    
    connection = sqlite3.connect('file::memory:', uri=True)

    def __init__(self):
        try:
            with self.connection:
                self.connection.row_factory = sqlite3.Row
                cursor = self.connection.cursor()
                for f in ['kjv_bible_books', 'kjv_bible_verses', 'kjv_bible_daily_verses', 'kjv_bible_daily_roberts']:
                    sql = open('../data/' + f + '.sql', encoding='utf-8')
                    cursor.executescript(sql.read())
                self.connection.commit()
        except Exception as e:
            print(e)
            
    def __del__(self):
        self.connection.close()
        
    def kjvBook(self, rstBook):
        cursor = self.connection.cursor()
        cursor.execute("select * from rst_bible_books where alt == :alt", {"alt": rstBook})
        row = cursor.fetchone()
        if row == None:
            raise NameError("Book missing: " + rstBook)
        cursor.execute("select * from kjv_bible_books where id == :id", {"id": row["id"]})
        row = cursor.fetchone()
    
        if row["id"] == None:
            raise NameError("Book missing: " + rstBook)

        return row["alt"]
        
    def kjvBookId(self, book):
        cursor = self.connection.cursor()
        cursor.execute("select * from kjv_bible_books where alt == :alt", {"alt": book})
        row = cursor.fetchone()
        if row == None or row["id"] == None:
            raise NameError("Book missing: " + book)
        return row["id"]
        
    def validate(self):
        try:
            with self.connection:
                cursor = self.connection.cursor()
                rows = cursor.execute('select * from kjv_bible_daily;').fetchall()
                for row in rows:
                    v = row['verses']
                    #print(v)
                    m = Parser.matches(v)
                    for ref in m:
                        book = self.kjvBookId(ref.name)
                        #print(book)
                        for loc in ref.locations:
                            if len(loc.verses) == 0 or len(loc.chapters) > 1:
                                print("full chapter(s)")
                            else:
                                fmt = 'select count(*) from kjv_bible where book_id == {book_id} and chapter == {chapter} and verse in ({list})'.format(book_id=book, chapter=loc.chapters[0], list=','.join(['?']*len(loc.verses)))
                                c = self.connection.cursor()
                                fet = c.execute(fmt, loc.verses)
                                count = fet.fetchone()['count(*)']
                                #print("verses set: ", loc.verses)
                                #print(count)
                                if len(loc.verses) != count:
                                    #print(v, ref)
                                    print("Invalid result for", ref.name, loc.chapters, loc.verses, count, v)
        except Exception as e:
            print(e)
            
    def showAllDaily(self):
        try:
            with self.connection:
                cursor = self.connection.cursor()
    
                rows = cursor.execute('select * from rst_bible_daily;')
                for row in rows:
                    v = row["verses"]
                    m = Parser.matches(v)
                    b = list(map(lambda x: x['Book'], m))
                    s = v
                    for book in b:
                        try:
                            s = s.replace(book, self.kjvBook(book))
                        except Exception as e:
                            print(row["month"], row["day"], e)
                            continue
            
                    print("({:02}, {:02}, {}, {}, '{}'),"
                    .format(row["month"], row["day"], row["morning"], row["evening"], s))
        except Exception as e:
            print(e)

    def showAllYear(self):
        try:
            with self.connection:
                cursor = self.connection.cursor()

                rows = cursor.execute('select * from rst_bible_daily_roberts;')
                for row in rows:
                    v = row["verses"]
                    m = Parser.matches(v)
                    b = list(map(lambda x: x['Book'], m))
                    s = v
                    for book in b:
                        try:
                            s = s.replace(book, self.kjvBook(book))
                        except Exception as e:
                            print(row["month"], row["day"], e)
                            continue
        
                    print("({:02}, {:02}, '{}'),".format(row["month"], row["day"], s))
        except Exception as e:
            print(e)

if __name__ == '__main__':
    BookMap().validate()
