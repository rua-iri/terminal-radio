package extra

import (
	"github.com/rua-iri/terminal-radio/internal/database"
	"github.com/rua-iri/terminal-radio/internal/utils"
)

func GetStatistics() {
	top5Stations := database.GetStatsTop5()
	utils.ShowTable(top5Stations)
}
