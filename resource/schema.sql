PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "stations" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"url"	TEXT NOT NULL,
	"img"	TEXT,
	"is_yt"	INTEGER NOT NULL,
	"is_active"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO stations VALUES(1,'BBC World Service','https://a.files.bbci.co.uk/ms6/live/3441A116-B12E-4D2F-ACA8-C1984642FA4B/audio/simulcast/hls/nonuk/audio_syndication_low_sbr_v1/cfs/bbc_world_service.m3u8','https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/BBC_World_Service_2022_(Boxed).svg/500px-BBC_World_Service_2022_(Boxed).svg.png',0,1);
CREATE TABLE IF NOT EXISTS "last_station" (
	"id"	INTEGER UNIQUE,
	"station_id"	INTEGER,
	"timestamp"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("station_id") REFERENCES "stations"("id")
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('stations',1);
COMMIT;
