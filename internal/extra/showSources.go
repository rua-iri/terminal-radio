package extra

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/rua-iri/terminal-radio/internal/database"
)

func ShowStations() {

	allStations := database.GetAllStations()

	jsonData, err := json.MarshalIndent(allStations, "", "  ")

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(string(jsonData))
}
