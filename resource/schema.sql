CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "stations" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"url"	TEXT NOT NULL,
	"img"	TEXT,
	"is_yt"	INTEGER NOT NULL,
	"is_active"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
