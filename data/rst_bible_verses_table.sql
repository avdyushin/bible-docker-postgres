--
-- Russian Synodal Translation
-- PostgreSQL dump by Grigory Avdyushin <avdyushin.g@gmail.com>
--

DROP TABLE IF EXISTS rst_bible;

CREATE TABLE rst_bible (
    book_id SMALLINT NOT NULL,
    chapter SMALLINT NOT NULL,
    verse   SMALLINT NOT NULL,
    text    TEXT NOT NULL,
    PRIMARY KEY (book_id, chapter, verse)
);
