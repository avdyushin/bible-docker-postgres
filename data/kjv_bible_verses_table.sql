--
-- King James Version
-- Converted from Unbound Bible by Grigory Avdyushin <avdyushin.g@gmail.com>
--

DROP TABLE IF EXISTS kjv_bible;

CREATE TABLE kjv_bible (
    book_id SMALLINT NOT NULL,
    chapter SMALLINT NOT NULL,
    verse   SMALLINT NOT NULL,
    text    TEXT NOT NULL,
    PRIMARY KEY (book_id, chapter, verse)
);
