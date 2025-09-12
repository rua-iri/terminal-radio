package database

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

func Main() {

	db, err := sql.Open("sqlite3", "./test.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	sqlStmt := `
	CREATE TABLE IF NOT EXISTS users (
	    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	    name TEXT
	);
	`

	_, err = db.Exec(sqlStmt)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Table 'users' created successfully")
}

func GetAllStations() []map[string]any {
	db, err := sql.Open("sqlite3", "./resource/radio_sources.sqlite")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	sqlStmt := `
	SELECT name,
        url, img, is_yt
        FROM stations
        WHERE is_active=1;
	`

	rows, err := db.Query(sqlStmt)

	if err != nil {
		log.Fatal(err)
	}

	cols, err := rows.Columns()

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(cols)

	results := []map[string]any{}

	for rows.Next() {
		values := make([]any, len(cols))
		valuePtrs := make([]any, len(cols))

		for i := range values {
			valuePtrs[i] = &values[i]
		}

		if err := rows.Scan(valuePtrs...); err != nil {
			log.Fatal(err)
		}

		rowMap := make(map[string]any, len(cols))

		for i, col := range cols {
			if b, ok := values[i].([]byte); ok {
				rowMap[col] = string(b)
			} else {
				rowMap[col] = values[i]
			}

			results = append(results, rowMap)
		}

	}

	return results

}
