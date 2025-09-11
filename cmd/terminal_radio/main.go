package main

import (
	"fmt"
	"os"
)

func initialiseLogs() {
	fmt.Println("Initialising Logs")
}

func main() {
	initialiseLogs()

	actions := map[string]func(){
		"hello":   initialiseLogs,
		"goodbye": initialiseLogs,
	}

	// cmdMap := map[string]func(){
	// 	"play":   radio.main,
	// 	"update": update_sources.main,
	// 	"logs":   show_logs,
	// 	"show":   show_stations,
	// 	"stats":  statistics.main,
	// 	"help":   show_help,
	// }

	var userCmd string

	if len(os.Args) < 2 {
		userCmd = "play"
	} else {
		userCmd = os.Args[1]
	}

	fmt.Println(userCmd)

	actions["hello"]()

}
