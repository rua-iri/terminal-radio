package main

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/rua-iri/terminal-radio/internal/database"
	"github.com/rua-iri/terminal-radio/internal/ui"
)

func getStatistics() {
	top5Stations := database.GetStatsTop5()
	ui.ShowTable(top5Stations)
}

func showStations() {
	allStations := database.GetAllStations()

	jsonData, err := json.MarshalIndent(allStations, "", "  ")
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(string(jsonData))
}

func showLogs() {
	fmt.Println("Not yet implemented")
}
