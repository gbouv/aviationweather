package main

import (
	"fmt"
	"os"
	"time"

	"github.com/gbouv/aviationweather/model"
)

func main() {
	started_time := time.Now()
	rawXml, err := os.ReadFile("../testdata/metars.xml")
	if err != nil {
		panic(err)
	}
	metars, err := model.ParseMetars(rawXml)
	if err != nil {
		panic(err)
	}
	for _, metar := range metars.Data.Metars {
		fmt.Println(metar.RawText)
	}
	fmt.Println("Time elapsed:", time.Since(started_time))
}
