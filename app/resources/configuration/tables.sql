CREATE TABLE Artist (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NULL
);

CREATE TABLE Song (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        id_artist INT NULL,
        title VARCHAR(100) NOT NULL,
        body TEXT NOT NULL,
        CONSTRAINT FK_artist FOREIGN KEY (id_artist) REFERENCES artist (id)
);