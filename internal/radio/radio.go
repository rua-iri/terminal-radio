package radio

import (
	"encoding/json"
	"fmt"
	"image"
	_ "image/jpeg"
	_ "image/png"
	"log"
	"net/http"
	"os"
	"os/exec"

	"github.com/charmbracelet/x/term"
	"github.com/mattn/go-sixel"
	"github.com/nfnt/resize"
	"github.com/rua-iri/terminal-radio/internal/database"
	"github.com/rua-iri/terminal-radio/internal/utils"
)

func getYTThumbnail(streamURL string) string {
	jsondata, err := exec.Command("yt-dlp", streamURL, "-j").Output() // .thumbnail

	if err != nil {
		log.Fatal(err)
	}

	var result map[string]interface{}
	json.Unmarshal(jsondata, &result)

	return result["thumbnail"].(string)
}

func displayImageSixel(imageUrl string) {

	const charHeight int = 20
	const charWidth int = 10
	termCols, termRows, err := term.GetSize(os.Stdout.Fd())
	termRows -= 5 // remove 5 because of the text output below image
	var widthPx int = termCols * charWidth
	var heightPx int = termRows * charHeight

	if err != nil {
		log.Fatal(err)
	}

	res, err := http.Get(imageUrl)

	if err != nil {
		log.Fatal(err)
	}
	defer res.Body.Close()

	img, _, err := image.Decode(res.Body)

	if err != nil {
		log.Fatal(err)
	}

	resizedImg := resize.Thumbnail(uint(widthPx), uint(heightPx), img, resize.Lanczos2)

	if err := sixel.NewEncoder(os.Stdout).Encode(resizedImg); err != nil {
		log.Fatal(err)
	}

}

func playRadio() {
	allStations := database.GetAllStations()

	var stationsList []string = []string{}
	var lastStationName string = database.GetLastStation()
	var lastStationIndex int

	for index, station := range allStations {
		if lastStationName == station["name"] {
			lastStationIndex = index
		}
		stationsList = append(stationsList, station["name"].(string))
	}

	var selectedStationName string = MainMenu(stationsList, lastStationIndex)

	if selectedStationName == "" {
		return
	}

	var selectedStation map[string]interface{}

	for _, station := range allStations {
		if station["name"] == selectedStationName {
			selectedStation = station
			break
		}
	}

	database.SetLastStation(selectedStationName)

	utils.ClearTerminal()
	var cmd *exec.Cmd

	if selectedStation["is_yt"] == int64(1) {
		// cmd = exec.Command("mpv", selectedStation["url"].(string), "--vo=sixel", "--really-quiet")
		selectedStation["img"] = getYTThumbnail(selectedStation["url"].(string))
	}

	displayImageSixel(selectedStation["img"].(string))
	cmd = exec.Command("mpv", selectedStation["url"].(string), "--no-video")

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
	utils.ClearTerminal()
	playRadio()
}
