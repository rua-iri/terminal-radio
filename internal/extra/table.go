package extra

import (
	"fmt"
	"os"
	"strconv"

	"github.com/charmbracelet/bubbles/table"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

var baseStyle = lipgloss.NewStyle().
	BorderStyle(lipgloss.NormalBorder()).
	BorderForeground(lipgloss.Color("240"))

type model struct {
	table table.Model
}

func (m model) Init() tea.Cmd { return nil }

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	return m, tea.Quit
}

func (m model) View() string {
	return baseStyle.Render(m.table.View()) + "\n"
}

func ShowTable(columnHeaders []string, top5StationsArray []map[string]any) {
	columns := []table.Column{
		{Title: "Index", Width: 10},
	}

	for _, columnHead := range columnHeaders {
		columns = append(columns, table.Column{Title: columnHead, Width: 20})
	}

	rows := []table.Row{}

	for index, rowItem := range top5StationsArray {
		var rowIndex int = index + 1
		rows = append(rows,
			table.Row{
				strconv.Itoa(rowIndex),
				rowItem["Station Name"].(string),
				strconv.FormatInt(rowItem["Play Count"].(int64), 10),
			},
		)
	}

	t := table.New(
		table.WithColumns(columns),
		table.WithRows(rows),
		table.WithFocused(true),
		table.WithHeight(7),
	)

	s := table.DefaultStyles()
	s.Header = s.Header.
		BorderStyle(lipgloss.NormalBorder()).
		BorderForeground(lipgloss.Color("240")).
		BorderBottom(true).
		Bold(false)
	s.Selected = s.Selected.
		Foreground(lipgloss.Color("229")).
		Background(lipgloss.Color("57")).
		Bold(false)
	t.SetStyles(s)

	m := model{t}
	if _, err := tea.NewProgram(m).Run(); err != nil {
		fmt.Println("Error running program:", err)
		os.Exit(1)
	}
}
