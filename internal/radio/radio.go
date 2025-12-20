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

func getYTStreamName(streamURL string) string {
	jsondata, err := exec.Command("yt-dlp", streamURL, "-j").Output() // .thumbnail

	if err != nil {
		log.Fatal(err)
	}

	var result map[string]interface{}
	json.Unmarshal(jsondata, &result)

	return result["fulltitle"].(string)
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

func initialiseTTY() *tty.TTY {
	tty, err := tty.Open()
	if err != nil {
		log.Fatal(err)
	}
	defer tty.Close()

	return tty
}

func playRadio() {
	allStations := database.GetAllStations()

	var stationsList []string = []string{}
	var lastStationName string = database.GetLastStation()
	var lastStationIndex int

	// Create a list of all station names
	// and get the starting index based on the last station
	for index, station := range allStations {
		if lastStationName == station["name"] {
			lastStationIndex = index
		}
		stationsList = append(stationsList, station["name"].(string))
	}

	var selectedStationName string = utils.MainMenu(stationsList, lastStationIndex)

	if selectedStationName == "" {
		os.Exit(0)
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
		// cmd = exec.Command("mpv", selectedaStation["url"].(string), "--vo=sixel", "--really-quiet")
		selectedStation["img"] = getYTThumbnail(selectedStation["url"].(string))
		selectedStation["name"] = getYTStreamName(selectedStation["url"].(string))
	}

	cmd = exec.Command("mpv", selectedStation["url"].(string), "--no-video")
	cmd.Start()

	displayImageSixel(selectedStation["img"].(string))
	fmt.Println()
	fmt.Printf("\nNow Playing: %s\n\n", selectedStation["name"])
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
			cmd = exec.Command("mpv", selectedStation["url"].(string), "--no-video")
			cmd.Start()
		}
	}

	fmt.Println("Quitting...")

}

func Main() {
	// run in a loop until exited by the user
	for {
		utils.ClearTerminal()
		playRadio()
	}
}
