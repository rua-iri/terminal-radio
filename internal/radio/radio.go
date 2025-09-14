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

	exec.Command("wget", "-O", "/tmp/terminalradio_img.png", selectedStation["img"].(string)).Start()
	cmd := exec.Command("img2sixel", "/tmp/terminalradio_img.png")
	cmd.Run()
	fmt.Println(cmd.Stdout)
	fmt.Println(exec.Command("ls", "-l").Output())

	// cmd := exec.Command("mpv", selectedStation["url"].(string))
	// cmd.Start()
	// fmt.Println("Now Playing", selectedStation["name"])
	// fmt.Println("Enter 'q' to exit")

	// var userInput string

	// for userInput != "q" {
	// 	fmt.Scan(&userInput)
	// 	fmt.Println(userInput)
	// }

	// cmd.Process.Kill()

}

func Main() {
	play_radio()
}
