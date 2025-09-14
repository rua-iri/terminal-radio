package database

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

const databaseFlavour string = "sqlite3"
const databaseName string = "./resource/radio_sources.sqlite"

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
	db, err := sql.Open(databaseFlavour, databaseName)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	const sqlStatement string = `
	SELECT name,
        url, img, is_yt
        FROM stations
        WHERE is_active=1;
	`

	rows, err := db.Query(sqlStatement)

	if err != nil {
		log.Fatal(err)
	}

	cols, err := rows.Columns()

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(cols)

	results := formatMapList(rows, cols)

	return results

}

func GetStatsTop5() []map[string]any {

	db, err := sql.Open(databaseFlavour, databaseName)

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

	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	rows, err := db.Query(sqlStatement)

	if err != nil {
		log.Fatal(err)
	}

	cols, err := rows.Columns()
	if err != nil {
		log.Fatal(err)
	}

	results := formatMapList(rows, cols)

	fmt.Println(results)

	return results
}
