package utils

import (
	"fmt"
	"log"
	"sort"
	"strings"

	"github.com/rua-iri/terminal-radio/internal/database"
)

var stationsList []string = []string{}

func ValidateStationInput(stationData map[string]string) {
	if stationData["url"] == "" || stationData["name"] == "" || stationData["isYT"] == "" {
		log.Fatal("Required Station Data Missing")
	}
}

func yesNoHumanToBool(yesNoValue string) bool {
	return strings.Contains("yes", strings.ToLower(yesNoValue))
}

func createStation() {
	fmt.Println("Creating new station")
	var newStationData map[string]string = MainTextForm("", "", "", "")

	isYT := yesNoHumanToBool(newStationData["isYT"])

	ValidateStationInput(newStationData)

	database.CreateStation(
		newStationData["name"],
		newStationData["url"],
		newStationData["img"],
		isYT,
	)

	fmt.Println("Station Added:", newStationData["name"])
}

func updateStation() {
	stationChoiceName := MainMenu(stationsList, 0)
	stationID := database.GetStationID(stationChoiceName)

	fmt.Println("Updating: ", stationChoiceName)

	var newStationData map[string]string = MainTextForm(
		database.GetStationDetails(stationChoiceName),
	)

	isYT := yesNoHumanToBool(newStationData["isYT"])

	ValidateStationInput(newStationData)

	database.UpdateStation(stationID, newStationData["name"], newStationData["url"], newStationData["img"], isYT)

}

func deleteStation() {
	stationChoiceName := MainMenu(stationsList, 0)
	database.DeleteStation(stationChoiceName)

	fmt.Println("Station Deleted:", stationChoiceName)
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
