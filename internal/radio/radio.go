package radio

import (
	"fmt"
	"reflect"

	"github.com/charmbracelet/bubbles/list"
)

func play_radio() {
	fmt.Println("Playing Radio...")
	items := []list.Item{
		item("Ramen"),
		item("Tomato Soup"),
		item("Hamburgers"),
		item("Cheeseburgers"),
		item("Currywurst"),
		item("Okonomiyaki"),
		item("Pasta"),
		item("Fillet Mignon"),
		item("Caviar"),
		item("Just Wine"),
	}
	var answer string = MainMenu(items)

	fmt.Println("'", answer, "'")
	fmt.Println(reflect.TypeOf(answer))
}

func Main() {
	play_radio()
}
