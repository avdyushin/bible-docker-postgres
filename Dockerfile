FROM postgres
MAINTAINER <avdyushin.g@gmail.com>

COPY data/rst_bible_books.sql /docker-entrypoint-initdb.d/10-rst-bible-books.sql
COPY data/rst_bible_verses.sql /docker-entrypoint-initdb.d/20-rst-bible-verses.sql
COPY data/rst_bible_daily_verses.sql /docker-entrypoint-initdb.d/30-rst-bible-daily-verses.sql
COPY data/rst_bible_daily_roberts.sql /docker-entrypoint-initdb.d/40-rst-bible-daily-reading.sql
