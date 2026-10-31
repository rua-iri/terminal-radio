package database

import (
	"database/sql"
	"log"
	"os"
	"path/filepath"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

const databaseFlavour string = "sqlite3"
const relativeDatabasePath string = "resource/radio_sources.sqlite"

var DB *sql.DB

type Station struct {
	Name string `json:"name"`
	URL  string `json:"url"`
	Img  string `json:"img"`
	IsYT bool   `json:"is_yt"`
}

// StationStat represents a row from the play-count statistics query.
type StationStat struct {
	Name      string
	PlayCount int64
}

func getDatabasePath() string {
	execPath, err := os.Executable()
	if err != nil {
		log.Fatal(err)
	}

	execPath, err = filepath.EvalSymlinks(execPath)
	if err != nil {
		log.Fatal(err)
	}
	return filepath.Join(filepath.Dir(execPath), relativeDatabasePath)
}

func Init_DB() {
	var err error
	DB, err = sql.Open(databaseFlavour, getDatabasePath())
	if err != nil {
		log.Fatal(err)
	}

	DB.SetMaxOpenConns(1)
	DB.SetMaxIdleConns(1)

}

func GetAllStations() []Station {
	const sqlStatement string = `
	SELECT name,
        url, img, is_yt
        FROM stations
        WHERE is_active=1;
	`

	rows, err := DB.Query(sqlStatement)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	var results []Station
	for rows.Next() {
		var station Station
		var isYT int64
		if err := rows.Scan(&station.Name, &station.URL, &station.Img, &isYT); err != nil {
			log.Fatal(err)
		}
		station.IsYT = isYT == 1
		results = append(results, station)
	}

	return results
}

func GetStatsTop5() []StationStat {
	const sqlStatement string = `
	SELECT stations.name as 'Station Name',
        count(last_station.id) AS "Play Count"
        FROM last_station
        INNER JOIN stations
        ON last_station.station_id = stations.id
        GROUP BY station_id
        ORDER BY "Play Count" DESC
        LIMIT 5;
	`

	rows, err := DB.Query(sqlStatement)
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	var results []StationStat
	for rows.Next() {
		var stationStatistics StationStat
		if err := rows.Scan(&stationStatistics.Name, &stationStatistics.PlayCount); err != nil {
			log.Fatal(err)
		}
		results = append(results, stationStatistics)
	}

	return results
}

func GetStationID(stationName string) int {
	const sqlStatement string = `
	SELECT id FROM stations WHERE name = ?;
	`

	result, err := DB.Query(sqlStatement, stationName)

	if err != nil {
		log.Fatal(err)
	}

	var id int
	result.Next()
	result.Scan(&id)
	result.Close()

	return id
}

func GetStationDetails(stationName string) Station {
	const sqlStatement string = `
	SELECT name, url, img, is_yt FROM stations WHERE stations.name = ? AND stations.is_active = 1;
	`
	row := DB.QueryRow(sqlStatement, stationName)

	var station Station
	var isYT int64
	row.Scan(&station.Name, &station.URL, &station.Img, &isYT)
	station.IsYT = isYT == 1

	return station
}

func GetLastStation() string {
	const sqlStatement string = `
	SELECT stations.name
        FROM last_station
        INNER JOIN stations
        ON last_station.station_id = stations.id
        ORDER BY last_station.id DESC
        LIMIT 1;
	`

	result, err := DB.Query(sqlStatement)

	if err != nil {
		log.Fatal(err)
	}

	var name string
	result.Next()
	result.Scan(&name)
	result.Close()

	return name
}

func SetLastStation(name string) {
	var currentStationID int = GetStationID(name)

	currentTimestamp := time.Now().Unix()

	const sqlStatement = `
	INSERT INTO last_station
	    (station_id, timestamp)
	    VALUES
	    (?, ?);
	`

	var err error
	_, err = DB.Exec(sqlStatement, currentStationID, currentTimestamp)

	if err != nil {
		log.Fatal(err)
	}

}

func CreateStation(name string, url string, img string, isYT bool) {
	const sqlStatement string = `
	INSERT INTO
        stations (name, url, img, is_yt, is_active)
        VALUES (?, ?, ?, ?, ?)
	`

	var err error
	_, err = DB.Exec(sqlStatement, name, url, img, isYT, true)

	if err != nil {
		log.Fatal(err)
	}

}

func UpdateStation(id int, name string, url string, img string, isYT bool) {
	const sqlStatement string = `
	UPDATE stations
        SET name=?, url=?, img=?, is_yt=?
        WHERE id=?
	`
	var err error
	_, err = DB.Exec(sqlStatement, name, url, img, isYT, id)

	if err != nil {
		log.Fatal(err)
	}

}

func DeleteStation(name string) {
	var currentStationID int = GetStationID(name)
	const sqlStatement string = `
	UPDATE stations
        SET is_active=0
        WHERE id=?
	`

	var err error
	_, err = DB.Exec(sqlStatement, currentStationID)

	if err != nil {
		log.Fatal(err)
	}

}
