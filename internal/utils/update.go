package utils

import (
	"fmt"
	"log"
	"sort"
	"strings"

	"github.com/rua-iri/terminal-radio/internal/database"
)

func ValidateStationInput(stationData map[string]string) {
	if stationData["url"] == "" || stationData["name"] == "" || stationData["isYT"] == "" {
		log.Fatal("Required Station Data Missing")
	}
}

func yesNoHumanToBool(yesNoValue string) bool {
	return strings.Contains("yes", strings.ToLower(yesNoValue))
}

func boolToYesNo(b bool) string {
	if b {
		return "yes"
	}
	return "no"
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

func updateStation(stationsList []string) {
	stationChoiceName := MainMenu(stationsList, 0)
	stationID := database.GetStationID(stationChoiceName)

	fmt.Println("Updating: ", stationChoiceName)

	existing := database.GetStationDetails(stationChoiceName)
	var newStationData map[string]string = MainTextForm(
		existing.Name,
		existing.URL,
		existing.Img,
		boolToYesNo(existing.IsYT),
	)

	isYT := yesNoHumanToBool(newStationData["isYT"])

	ValidateStationInput(newStationData)

	database.UpdateStation(stationID, newStationData["name"], newStationData["url"], newStationData["img"], isYT)
}

func deleteStation(stationsList []string) {
	stationChoiceName := MainMenu(stationsList, 0)
	database.DeleteStation(stationChoiceName)

	fmt.Println("Station Deleted:", stationChoiceName)
}

func UpdateSources() {
	allStations := database.GetAllStations()

	var stationsList []string = []string{}
	for _, station := range allStations {
		stationsList = append(stationsList, station.Name)
	}

	updateOptions := map[string]func(){
		"Add a new source":          createStation,
		"Remove an existing source": func() { deleteStation(stationsList) },
		"Edit an existing source":   func() { updateStation(stationsList) },
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
