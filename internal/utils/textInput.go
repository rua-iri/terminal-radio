package utils

// A simple example demonstrating the use of multiple text input components
// from the Bubbles component library.

import (
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/charmbracelet/bubbles/cursor"
	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

var (
	focusedStyle        = lipgloss.NewStyle().Foreground(lipgloss.Color(MENU_COLOUR_PRIMARY))
	blurredStyle        = lipgloss.NewStyle().Foreground(lipgloss.Color(MENU_COLOUR_SECONDARY))
	cursorStyle         = focusedStyle
	noStyle             = lipgloss.NewStyle()
	textHelpStyle       = blurredStyle
	cursorModeHelpStyle = lipgloss.NewStyle().Foreground(lipgloss.Color(MENU_COLOUR_GREY))

	focusedButton = focusedStyle.Render("[ Submit ]")
	blurredButton = fmt.Sprintf("[ %s ]", blurredStyle.Render("Submit"))
)

type textModel struct {
	focusIndex int
	inputs     []textinput.Model
	cursorMode cursor.Mode
}

func initialModel(stationName string, stationURL string, stationImg string, isYT string) textModel {
	m := textModel{
		inputs: make([]textinput.Model, 4),
	}

	var t textinput.Model
	for i := range m.inputs {
		t = textinput.New()
		t.Cursor.Style = cursorStyle
		t.CharLimit = 150
		t.Width = 150

		switch i {
		case 0:
			t.Placeholder = "Station Name"
			t.Focus()
			t.PromptStyle = focusedStyle
			t.TextStyle = focusedStyle
			t.SetValue(stationName)
		case 1:
			t.Placeholder = "Station URL"
			t.SetValue(stationURL)
		case 2:
			t.Placeholder = "Station Image"
			t.SetValue(stationImg)
		case 3:
			t.Placeholder = "Is Station YT (yes/no)"
			t.CharLimit = 3
			t.SetValue(isYT)
		}

		m.inputs[i] = t
	}

	return m
}

func (m textModel) Init() tea.Cmd {
	return textinput.Blink
}

func (m textModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "esc":
			return m, tea.Quit

		// Change cursor mode
		case "ctrl+r":
			m.cursorMode++
			if m.cursorMode > cursor.CursorHide {
				m.cursorMode = cursor.CursorBlink
			}
			cmds := make([]tea.Cmd, len(m.inputs))
			for i := range m.inputs {
				cmds[i] = m.inputs[i].Cursor.SetMode(m.cursorMode)
			}
			return m, tea.Batch(cmds...)

		// Set focus to next input
		case "tab", "shift+tab", "enter", "up", "down":
			s := msg.String()

			// Did the user press enter while the submit button was focused?
			// If so, exit.
			if s == "enter" && m.focusIndex == len(m.inputs) {
				return m, tea.Quit
			}

			// Cycle indexes
			if s == "up" || s == "shift+tab" {
				m.focusIndex--
			} else {
				m.focusIndex++
			}

			if m.focusIndex > len(m.inputs) {
				m.focusIndex = 0
			} else if m.focusIndex < 0 {
				m.focusIndex = len(m.inputs)
			}

			cmds := make([]tea.Cmd, len(m.inputs))
			for i := 0; i <= len(m.inputs)-1; i++ {
				if i == m.focusIndex {
					// Set focused state
					cmds[i] = m.inputs[i].Focus()
					m.inputs[i].PromptStyle = focusedStyle
					m.inputs[i].TextStyle = focusedStyle
					continue
				}
				// Remove focused state
				m.inputs[i].Blur()
				m.inputs[i].PromptStyle = noStyle
				m.inputs[i].TextStyle = noStyle
			}

			return m, tea.Batch(cmds...)
		}
	}

	// Handle character input and blinking
	cmd := m.updateInputs(msg)

	return m, cmd
}

func (m *textModel) updateInputs(msg tea.Msg) tea.Cmd {
	cmds := make([]tea.Cmd, len(m.inputs))

	// Only text inputs with Focus() set will respond, so it's safe to simply
	// update all of them here without any further logic.
	for i := range m.inputs {
		m.inputs[i], cmds[i] = m.inputs[i].Update(msg)
	}

	return tea.Batch(cmds...)
}

func (m textModel) View() string {
	var b strings.Builder

	for i := range m.inputs {
		b.WriteString(m.inputs[i].View())
		if i < len(m.inputs)-1 {
			b.WriteRune('\n')
		}
	}

	button := &blurredButton
	if m.focusIndex == len(m.inputs) {
		button = &focusedButton
	}
	fmt.Fprintf(&b, "\n\n%s\n\n", *button)

	b.WriteString(textHelpStyle.Render("cursor mode is "))
	b.WriteString(cursorModeHelpStyle.Render(m.cursorMode.String()))
	b.WriteString(textHelpStyle.Render(" (ctrl+r to change style)"))

	return b.String()
}

func (m textModel) Values() map[string]string {

	if len(m.inputs) != 4 {
		log.Fatal("Not enough inputs")
	}

	valuesMap := map[string]string{
		"name": m.inputs[0].Value(),
		"url":  m.inputs[1].Value(),
		"img":  m.inputs[2].Value(),
		"isYT": m.inputs[3].Value(),
	}

	return valuesMap
}

func MainTextForm(stationName string, stationURL string, stationImg string, isYT string) map[string]string {
	p := tea.NewProgram(initialModel(stationName, stationURL, stationImg, isYT))

	finalModel, err := p.Run()

	if err != nil {
		fmt.Printf("Could not start program: %s\n", err)
		os.Exit(1)
	}

	fmt.Println(finalModel.(textModel).Values())

	return finalModel.(textModel).Values()

}
