#!/bin/sh

mkdir /tmp/bible/

cp ../data/kjv_bible_books.sql /tmp/bible/10-kjv-bible-books.sql
cp ../data/kjv_bible_verses_table.sql /tmp/bible/20-kjv-bible-verses-table.sql
cp ../data/kjv_bible_verses_data.sql /tmp/bible/21-kjv-bible-verses-data.sql
cp ../data/kjv_bible_daily_verses.sql /tmp/bible/30-kjv-bible-daily-verses.sql
cp ../data/kjv_bible_daily_roberts.sql /tmp/bible/40-kjv-bible-daily-reading.sql

cp ../data/rst_bible_books.sql /tmp/bible/50-rst-bible-books.sql
cp ../data/rst_bible_verses_table.sql /tmp/bible/60-rst-bible-verses-table.sql
cp ../data/rst_bible_verses_data.sql /tmp/bible/61-rst-bible-verses-data.sql

for f in /tmp/bible/*.sql; do
    sqlite3 /tmp/bible/temp.db < $f

    if [ $? -ne 0 ]; then
        rm /tmp/bible/temp.db
        exit -1
    fi
done

A="$(sqlite3 /tmp/bible/temp.db 'select count(*) from kjv_bible_books')"
B="$(sqlite3 /tmp/bible/temp.db 'select count(distinct book_id) from kjv_bible')"

if [ $A -ne $B ]; then
    exit -1
fi

echo "KJV: ${A} == ${B}"

A="$(sqlite3 /tmp/bible/temp.db 'select count(*) from rst_bible_books')"
B="$(sqlite3 /tmp/bible/temp.db 'select count(distinct book_id) from rst_bible')"

echo "RST: ${A} == ${B}"

rm -fr /tmp/bible

