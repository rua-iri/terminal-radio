package extra

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/rua-iri/terminal-radio/internal/database"
)

func ShowStations() {

	allStations := database.GetAllStations()

	// fmt.Println(allStations)
	// fmt.Println(reflect.TypeOf(allStations))

	jsonData, err := json.MarshalIndent(allStations, "", "  ")

	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(string(jsonData))
}
