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
	"github.com/mattn/go-tty"
	"github.com/nfnt/resize"
	"github.com/rua-iri/terminal-radio/internal/database"
	"github.com/rua-iri/terminal-radio/internal/ui"
)

func getYTData(streamURL string) map[string]string {

	var ytData map[string]string

	jsondata, err := exec.Command("yt-dlp", streamURL, "-j").Output() // .thumbnail

	if err != nil {
		log.Fatal(err)
	}

	var result map[string]interface{}
	json.Unmarshal(jsondata, &result)

	ytData = map[string]string{
		"img":  result["thumbnail"].(string),
		"name": result["fulltitle"].(string),
	}

	return ytData
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

	// Create a list of all station names
	// and get the starting index based on the last station
	for index, station := range allStations {
		if lastStationName == station.Name {
			lastStationIndex = index
		}
		stationsList = append(stationsList, station.Name)
	}

	var selectedStationName string = ui.MainMenu(stationsList, lastStationIndex)

	if selectedStationName == "" {
		os.Exit(0)
	}

	var selectedStation database.Station

	for _, station := range allStations {
		if station.Name == selectedStationName {
			selectedStation = station
			break
		}
	}

	database.SetLastStation(selectedStationName)

	ui.ClearTerminal()
	var cmd *exec.Cmd

	if selectedStation.IsYT {
		ytData := getYTData(selectedStation.URL)
		selectedStation.Img = ytData["img"]
		selectedStation.Name = ytData["name"]
	}

	cmd = exec.Command("mpv", selectedStation.URL, "--no-video")
	cmd.Start()

	displayImageSixel(selectedStation.Img)
	fmt.Println()
	fmt.Printf("\nNow Playing: %s\n\n", selectedStation.Name)
	fmt.Println("Press 'q' to exit")
	fmt.Println("Press 'r' to refresh")

	tty, err := tty.Open()
	if err != nil {
		log.Fatal(err)
	}
	defer tty.Close()

	// iterate until user has quit the stream
	for {
		r, err := tty.ReadRune()
		var userInput string = string(r)

		if err != nil {
			log.Fatal(err)
		}

		if userInput == "q" {
			cmd.Process.Kill()
			break
		} else if userInput == "r" {
			cmd.Process.Kill()
			cmd = exec.Command("mpv", selectedStation.URL, "--no-video")
			cmd.Start()
		}
	}

	fmt.Println("Quitting...")

}

func Main() {
	// run in a loop until exited by the user
	for {
		ui.ClearTerminal()
		playRadio()
	}
}
