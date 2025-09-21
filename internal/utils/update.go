package utils

import (
	"fmt"
	"sort"
	"strings"

	"github.com/rua-iri/terminal-radio/internal/database"
)

var stationsList []string = []string{}

func createStation() {
	fmt.Println("Creating new station")
	var newStationData map[string]string = MainTextInput()

	isYT := strings.Contains("yes", newStationData["isYT"])

	database.CreateStation(
		newStationData["name"],
		newStationData["url"],
		newStationData["img"],
		isYT,
	)

	fmt.Println("Station Added:", newStationData["name"])
}

func updateStation() {
	stationChoice := MainMenu(stationsList, 0)

	var stationName, stationURL, stationImg string
	fmt.Scan("Station Name", &stationName)
	fmt.Scan("Station URL", &stationURL)
	fmt.Scan("Station Img", &stationImg)

	fmt.Println("Updating: ", stationChoice)

	fmt.Println(stationName)
	fmt.Println(stationURL)
	fmt.Println(stationImg)
}

func deleteStation() {
	stationChoice := MainMenu(stationsList, 0)
	database.DeleteStation(stationChoice)
}

func UpdateSources() {

	updateOptions := map[string]func(){
		"Add a new source":          createStation,
		"Remove an existing source": deleteStation,
		"Edit an existing source":   updateStation,
	}

	allStations := database.GetAllStations()

	// Create a list of all station names
	for _, station := range allStations {
		stationsList = append(stationsList, station["name"].(string))
	}

	// Create a new array for the menu options
	updatekeys := make([]string, len(updateOptions))

	var index int = 0
	for key := range updateOptions {
		updatekeys[index] = key
		index++
	}

	// For some reason the array is sometimes
	// mixed up without this
	sort.Strings(updatekeys)

	updateChoice := MainMenu(updatekeys, 0)

	if updateChoice == "" {
		return
	}

	// Call the function based on the user's choice
	updateOptions[updateChoice]()
}
