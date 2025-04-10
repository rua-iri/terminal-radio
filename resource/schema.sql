CREATE TABLE IF NOT EXISTS "stations" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"url"	TEXT NOT NULL,
	"img"	TEXT,
	"is_yt"	INTEGER NOT NULL,
	"is_active"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "last_station" (
	"id"	INTEGER UNIQUE,
	"station_id"	INTEGER,
	"timestamp"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("station_id") REFERENCES "stations"("id")
);
