package radio

import (
	"fmt"
	"os/exec"
	"reflect"

	"github.com/rua-iri/terminal-radio/internal/database"
)

func play_radio() {
	fmt.Println("Playing Radio...")

	allStations := database.GetAllStations()

	var stationsList []string = []string{}

	for _, station := range allStations {
		stationsList = append(stationsList, station["name"].(string))
	}

	var selectedStationName string = MainMenu(stationsList)

	if selectedStationName == "" {
		return
	}

	fmt.Println("'", selectedStationName, "'")
	fmt.Println(reflect.TypeOf(selectedStationName))

	var selectedStation map[string]interface{}

	for _, station := range allStations {
		if station["name"] == selectedStationName {
			selectedStation = station
			break
		}
	}

	fmt.Println(selectedStation)
	fmt.Println(selectedStation["url"].(string))

	cmd := exec.Command("mpv", selectedStation["url"].(string))
	fmt.Println(cmd.Output())

}

func Main() {
	play_radio()
}
