package model

import (
	"encoding/xml"
	"time"
)

type Metars struct {
	XMLName xml.Name   `xml:"response"`
	Data    MetarsData `xml:"data"`
}

type MetarsData struct {
	XMLName    xml.Name `xml:"data"`
	NumResults int      `xml:"num_results,attr"`
	Metars     []Metar  `xml:"METAR"`
}

type Metar struct {
	XMLName                   xml.Name             `xml:"METAR"`
	RawText                   string               `xml:"raw_text"`
	StationId                 string               `xml:"station_id"`
	ObservationTime           time.Time            `xml:"observation_time"`
	Latitude                  *float64             `xml:"latitude"`
	Longitude                 *float64             `xml:"longitude"`
	TempC                     *float64             `xml:"temp_c"`
	DewpointC                 *float64             `xml:"dewpoint_c"`
	WindDirDegrees            *int                 `xml:"wind_dir_degrees"`
	WindSpeedKt               *int                 `xml:"wind_speed_kt"`
	WindGustKt                *int                 `xml:"wind_gust_kt"`
	VisibilityStatuteMi       *float64             `xml:"visibility_statute_mi"`
	AltimInHg                 *float64             `xml:"altim_in_hg"`
	SeeLevelPressureMb        *float64             `xml:"sea_level_pressure_mb"`
	QualityControlFlags       *QualityControlFlags `xml:"quality_control_flags"`
	SkyCondition              []SkyCondition       `xml:"sky_condition"`
	FlightCategory            *string              `xml:"flight_category"`
	ThreeHrPressureTendencyMb *float64             `xml:"three_hr_pressure_tendency_mb"`
	MaxTempC                  *float64             `xml:"maxT_c"`
	MinTempC                  *float64             `xml:"minT_c"`
	MaxTemp24HrC              *float64             `xml:"maxT24hr_c"`
	MinTemp24HrC              *float64             `xml:"minT24hr_c"`
	PrecipIn                  *float64             `xml:"precip_in"`
	Pcp3HrIn                  *float64             `xml:"pcp3hr_in"`
	Pcp6HrIn                  *float64             `xml:"pcp6hr_in"`
	Pcp24HrIn                 *float64             `xml:"pcp24hr_in"`
	SnowIn                    *float64             `xml:"snow_in"`
	VertVisFt                 *int                 `xml:"vert_vis_ft"`
	MetarType                 *string              `xml:"metar_type"`
	ElevationM                *float64             `xml:"elevation_m"`
}

type QualityControlFlags struct {
	XMLName                 xml.Name `xml:"quality_control_flags"`
	AutoStation             *string  `xml:"auto_station"`
	MaintenanceIndicatorOn  *string  `xml:"maintenance_indicator_on"`
	AutoStationType         *string  `xml:"auto_station_type"`
	NoSignal                *string  `xml:"no_signal"`
	LightningSensorOff      *string  `xml:"lightning_sensor_off"`
	FreezingRainSensorOff   *string  `xml:"freezing_rain_sensor_off"`
	PresentWeatherSensorOff *string  `xml:"present_weather_sensor_off"`
	SnowSensorOff           *string  `xml:"snow_sensor_off"`
}

type SkyCondition struct {
	XMLName        xml.Name `xml:"sky_condition"`
	SkyCover       string   `xml:"sky_cover,attr"`
	CloudBaseFtAgl *int     `xml:"cloud_base_ft_agl,attr"`
}

func ParseMetars(rawXml []byte) (*Metars, error) {
	var parsedXml Metars
	if err := xml.Unmarshal(rawXml, &parsedXml); err != nil {
		return nil, err
	}
	return &parsedXml, nil
}
