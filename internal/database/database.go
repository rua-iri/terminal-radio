package database

import (
	"database/sql"
	"log"
	"time"

	_ "github.com/mattn/go-sqlite3"
)

const databaseFlavour string = "sqlite3"
const databaseName string = "./resource/radio_sources.sqlite"

var DB *sql.DB

func Init_DB() {
	var err error
	DB, err = sql.Open(databaseFlavour, databaseName)
	if err != nil {
		log.Fatal(err)
	}

	DB.SetMaxOpenConns(1)
	DB.SetMaxIdleConns(1)

}

func formatMapList(rows *sql.Rows, columns []string) []map[string]any {
	results := []map[string]any{}

	for rows.Next() {
		values := make([]any, len(columns))
		valuePtrs := make([]any, len(columns))

		for i := range values {
			valuePtrs[i] = &values[i]
		}

		if err := rows.Scan(valuePtrs...); err != nil {
			log.Fatal(err)
		}

		rowMap := make(map[string]any, len(columns))

		for i, col := range columns {
			if b, ok := values[i].([]byte); ok {
				rowMap[col] = string(b)
			} else {
				rowMap[col] = values[i]
			}

		}
		results = append(results, rowMap)

	}

	return results
}

func GetAllStations() []map[string]any {
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

	cols, err := rows.Columns()

	if err != nil {
		log.Fatal(err)
	}

	results := formatMapList(rows, cols)
	rows.Close()

	return results

}

func GetStatsTop5() []map[string]any {
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

	cols, err := rows.Columns()
	if err != nil {
		log.Fatal(err)
	}

	results := formatMapList(rows, cols)
	rows.Close()

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
