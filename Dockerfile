FROM postgres
MAINTAINER <avdyushin.g@gmail.com>

COPY data/kjv_bible_books.sql /docker-entrypoint-initdb.d/10-kjv-bible-books.sql
COPY data/kjv_bible_verses.sql /docker-entrypoint-initdb.d/20-kjv-bible-verses.sql
COPY data/kjv_bible_daily_verses.sql /docker-entrypoint-initdb.d/30-kjv-bible-daily-verses.sql
COPY data/kjv_bible_daily_roberts.sql /docker-entrypoint-initdb.d/40-kjv-bible-daily-reading.sql

COPY data/rst_bible_books.sql /docker-entrypoint-initdb.d/50-rst-bible-books.sql
COPY data/rst_bible_verses.sql /docker-entrypoint-initdb.d/60-rst-bible-verses.sql
