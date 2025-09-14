package extra

import (
	"github.com/rua-iri/terminal-radio/internal/database"
)

func formatTable(top5StationsArray []map[string]any) {

}

func GetStatistics() {
	// 1. Get top 5 stations
	// 2. format table
	// 3. print table

	top5StationsArray := database.GetStatsTop5()

	stationsKeys := make([]string, len(top5StationsArray[0]))
	var i int = 0
	for k := range top5StationsArray[0] {
		stationsKeys[i] = k
		i++
	}

	ShowTable(stationsKeys, top5StationsArray)

}
