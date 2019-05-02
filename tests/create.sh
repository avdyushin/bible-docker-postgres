#!/bin/sh

for f in ../data/*.sql; do
    sqlite3 /tmp/temp.db < $f

    if [ $? -ne 0 ]; then
        rm /tmp/temp.db
        exit -1
    fi
done

A="$(sqlite3 /tmp/temp.db 'select count(*) from kjv_bible_books')"
B="$(sqlite3 /tmp/temp.db 'select count(distinct book_id) from kjv_bible')"

if [ $A -ne $B ]; then
    exit -1
fi

echo "KJV: ${A} == ${B}"

A="$(sqlite3 /tmp/temp.db 'select count(*) from rst_bible_books')"
B="$(sqlite3 /tmp/temp.db 'select count(distinct book_id) from rst_bible')"

echo "RST: ${A} == ${B}"

rm /tmp/temp.db

