#!/usr/bin/python

from dataclasses import dataclass
import re
import sqlite3

@dataclass
class Location:
    chapters: [int]
    verses: [int]
    
@dataclass
class Reference:
    name: str
    locations: [Location]
    
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
        #for d in m:
        #    print(d)
        return m
            
class BookMap:
    
    connection = sqlite3.connect('file::memory:', uri=True)

    def __init__(self):
        try:
            with self.connection:
                self.connection.row_factory = sqlite3.Row
                cursor = self.connection.cursor()
                for f in ['rst_bible_books', 'kjv_bible_daily_verses', 'kjv_bible_daily_roberts', 'kjv_bible_books']:
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
    # print(Parser.matches("Быт 1:2,3-4 3:3 & Jh 1"))
    bmap = BookMap()
    bmap.showAllYear()