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

	helpCommands := []string{
		"%splay%s	- Run the application to listen to radio stations",
		"%supdate%s	- Update the list of available stations",
		"%slogs%s	- View the application's logs to debug issues",
		"%sshow%s	- Show a JSON formatted list of the currently available stations",
		"%sstats%s	- Show the top 5 stations by play count",
		"%shelp%s	- Display this help menu",
	}

	for index := range helpCommands {
		fmt.Printf(helpCommands[index]+"\n", utils.TERMINAL_COLOUR_GREEN, utils.TERMINAL_COLOUR_RESET)
	}

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
