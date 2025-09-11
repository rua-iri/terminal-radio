package radio

import (
	"fmt"
	"time"
)

func play_radio() {
	fmt.Println("Playing Radio...")
}

func Main() {

	for x := true; x != false; {
		play_radio()
		time.Sleep(2 * time.Second)
	}

}
