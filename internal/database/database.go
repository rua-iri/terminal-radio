package database

import (
	"database/sql"
	"fmt"
	"log"
	"reflect"

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

	var asdf *sql.DB = db
	fmt.Println(asdf)

	fmt.Println(reflect.TypeOf(db))

	_, err = db.Exec(sqlStmt)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("Table 'users' created successfully")
}
