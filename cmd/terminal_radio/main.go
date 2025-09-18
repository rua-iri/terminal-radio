package main

import (
	"fmt"
	"os"

	"github.com/rua-iri/terminal-radio/internal/database"
	"github.com/rua-iri/terminal-radio/internal/extra"
	"github.com/rua-iri/terminal-radio/internal/radio"
	"github.com/rua-iri/terminal-radio/internal/utils"
)

func initialiseLogs() {
	// fmt.Println("Initialising Logs")
}

func show_help() {
	const helpData string = `play	- Run the application to listen to radio stations
update	- Update the list of available stations
logs	- View the application's logs to debug issues
show	- Show a JSON formatted list of the currently available stations
stats	- Show the top 5 stations by play count
help	- Display this help menu`
	fmt.Println(helpData)
}

func main() {
	initialiseLogs()
	database.Init_DB()
	defer database.DB.Close()

	cmdMap := map[string]func(){
		"play":   radio.Main,
		"update": utils.UpdateSources,
		// "logs":   show_logs,
		"show":  extra.ShowStations,
		"stats": extra.GetStatistics,
		"help":  show_help,
	}

	var userCmd string

	if len(os.Args) < 2 {
		userCmd = "play"
	} else {
		userCmd = os.Args[1]
	}

	userFunc, isFuncInMAP := cmdMap[userCmd]

	if !isFuncInMAP {
		fmt.Printf("Error: '%s' not an argument\n", userCmd)
		fmt.Println()
		cmdMap["help"]()
		return
	}

	userFunc()

}
