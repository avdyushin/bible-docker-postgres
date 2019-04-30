# Bible Docker Postgres
## About

This is Bible texts in PostrgeSQL database packed into Docker container.
It has the Russian Synodal Translation [RST](https://en.wikipedia.org/wiki/Russian_Synodal_Bible) and
the King James Version [KJV](https://en.wikipedia.org/wiki/King_James_Version) versions.

Table names are start with bible version prefix:

### Book names

```sql
CREATE TABLE rst_bible_books (
    id   SMALLINT NOT NULL PRIMARY KEY,
    book VARCHAR(40) NOT NULL,
    alt  VARCHAR(20) NOT NULL,
    abbr VARCHAR(20) NOT NULL,
    UNIQUE (book, alt, abbr)
);
```

### Book verses

```sql
CREATE TABLE rst_bible (
    book_id SMALLINT NOT NULL,
    chapter SMALLINT NOT NULL,
    verse   SMALLINT NOT NULL,
    text    TEXT NOT NULL,
    PRIMARY KEY (book_id, chapter, verse)
);
```

### Verse of the day

```sql
CREATE TABLE rst_bible_daily (
    id      SERIAL PRIMARY KEY,
    month   SMALLINT NOT NULL,
    day     SMALLINT NOT NULL,
    morning VARCHAR(1) NOT NULL,
    evening VARCHAR(1) NOT NULL,
    verses  VARCHAR(1024) NOT NULL
);
```

You can get daily verses by month, day and daytime (morning or evening).
Verses goes in plain text with bible references: `Флп 3:13,14 Иоан 17:24; 2 Тим 1:12 Флп 1:6; 1 Кор 9:24,25 Евр 12:1,2`.

### Daily reading verses

```sql
CREATE TABLE rst_bible_daily_roberts (
    month  SMALLINT NOT NULL,
    day    SMALLINT NOT NULL,
    verses VARCHAR(128) NOT NULL,
    PRIMARY KEY (month, day)
);
```

This is Bible Companion by [Robert Roberts](https://en.wikipedia.org/wiki/Robert_Roberts_(Christadelphian)).

Verses for each day the year which covers while Bible in one year.
Verses in the same format as verse of the day.

## Run & build container

Use docker-compose:

```sh
docker-compose up
```

It will build image if needed:

```sh
Creating network "docker-rst-bible-db_network" with the default driver
Building db
Step 1/6 : FROM postgres
 ---> 7a2907672aab
Step 2/6 : MAINTAINER <avdyushin.g@gmail.com>
 ---> Using cache
 ---> 6c71816b832a
Step 3/6 : COPY data/rst_bible_books.sql /docker-entrypoint-initdb.d/10-rst-bible-books.sql
 ---> 5dd2349d357c
Step 4/6 : COPY data/rst_bible_verses.sql /docker-entrypoint-initdb.d/20-rst-bible-verses.sql
 ---> 820b96d3e5f0
Step 5/6 : COPY data/rst_bible_daily_verses.sql /docker-entrypoint-initdb.d/30-rst-bible-daily-verses.sql
 ---> 167827c99771
Step 6/6 : COPY data/rst_bible_daily_roberts.sql /docker-entrypoint-initdb.d/40-rst-bible-daily-reading.sql
 ---> da09204caa9b
Successfully built da09204caa9b
Successfully tagged docker-rst-bible-db_db:latest
WARNING: Image for service db was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
Creating docker-rst-bible-db_db_1 ... done
Attaching to docker-rst-bible-db_db_1
<...>
```

## Connect with Docker

Once it's run you can connect using docker (find container id first):

```sh
docker ps
```

Execute `psql`:

```sh
docker exec -it <container-id> psql -U docker -d bible
```

```sh
psql (11.0 (Debian 11.0-1.pgdg90+2))
Type "help" for help.

bible=# \c
You are now connected to database "bible" as user "docker".
bible=# \dt
                 List of relations
 Schema |          Name           | Type  | Owner
--------+-------------------------+-------+--------
 public | rst_bible               | table | docker
 public | rst_bible_books         | table | docker
 public | rst_bible_daily         | table | docker
 public | rst_bible_daily_roberts | table | docker
(4 rows)
```

## Connect with PostgreSQL client

Just connect to Docker's IP address to port `5432` with `docker` user and `docker` password.
Database name is `bible`.

## Bible source

Books in Unbound Bible format: [Unbound](http://unbound.biola.edu/index.cfm?method=downloads.showDownloadMain)

Converters to SQL format are [here](https://gist.github.com/avdyushin/0555221cb4703ca5ba4f55038d253964)

