package radio

import (
	"fmt"
	"image"
	_ "image/jpeg"
	_ "image/png"
	"log"
	"net/http"
	"os"
	"os/exec"
	"reflect"

	"github.com/mattn/go-sixel"
	"github.com/rua-iri/terminal-radio/internal/database"
	"github.com/rua-iri/terminal-radio/internal/utils"
)

func displayImageSixel(imageUrl string) {
	res, err := http.Get(imageUrl)

	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	img, _, err := image.Decode(res.Body)

	if err != nil {
		log.Fatal(err)
	}

	if err := sixel.NewEncoder(os.Stdout).Encode(img); err != nil {
		log.Fatal(err)
	}

}

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

	utils.ClearTerminal()
	displayImageSixel(selectedStation["img"].(string))

	cmd := exec.Command("mpv", selectedStation["url"].(string))
	cmd.Start()

	fmt.Println()
	fmt.Printf("\nNow Playing: %s\n\n", selectedStationName)
	fmt.Println("Enter 'q' to exit")

	var userInput string

	for userInput != "q" {
		fmt.Scan(&userInput)
	}

	fmt.Println("Quitting...")
	cmd.Process.Kill()

}

func Main() {
	play_radio()
}
