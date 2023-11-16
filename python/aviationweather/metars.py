from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import xml.etree.ElementTree as ET


class Metars:
    request_index: int
    data_source: str
    request: str
    errors: list[str] = []
    warnings: list[str] = []
    time_taken_ms: int
    data: MetarsData

    def __repr__(self) -> str:
        return self.__dict__.__repr__()


@dataclass
class MetarsData:
    num_results: int
    metars: list[Metar]

    def __repr__(self) -> str:
        return self.__dict__.__repr__()


class Metar:
    raw_text: str
    station_id: str
    observation_time_str: str
    observation_time: datetime.datetime
    latitude: Optional[float]
    longitude: Optional[float]
    temp_c: Optional[float]
    dewpoint_c: Optional[float]
    wind_dir_degrees: Optional[int]
    wind_speed_kt: Optional[int]
    wind_gust_kt: Optional[int]
    visibility_statute_mi: Optional[float]
    altim_in_hg: Optional[float]
    sea_level_pressure_mb: Optional[float]
    quality_control_flags: Optional[QualityControlFlag]
    sky_conditions: list[SkyCondition] = []
    flight_category: Optional[str]
    three_hr_pressure_tendency_mb: Optional[float]
    maxT_c: Optional[float]
    minT_c: Optional[float]
    maxT24hr_c: Optional[float]
    minT24hr_c: Optional[float]
    precip_in: Optional[float]
    pcp3hr_in: Optional[float]
    pcp6hr_in: Optional[float]
    pcp24hr_in: Optional[float]
    snow_in: Optional[float]
    vert_vis_ft: Optional[int]
    metar_type: Optional[str]
    elevation_m: Optional[float]

    def __repr__(self) -> str:
        return self.__dict__.__repr__()


class QualityControlFlag:
    auto_station: str
    maintenance_indicator_on: str

    def __repr__(self) -> str:
        return self.__dict__.__repr__()


class SkyCondition:
    sky_cover: str
    cloud_base_ft_agl: int

    def __repr__(self) -> str:
        return self.__dict__.__repr__()


def parse(xml_filename: str) -> Metars:
    mytree = ET.parse(xml_filename)
    myroot = mytree.getroot()

    metars = Metars()
    metars_data = MetarsData(num_results=0, metars=[])
    for elt in myroot:
        match elt.tag:
            case "request_index":
                metars.request_index = _parse_int(elt.text)
            case "data_source":
                metars.data_source = elt.attrib["name"]
            case "request":
                metars.request = elt.attrib["type"]
            case "errors":
                for child in elt:
                    metars.errors.append(child.text)
            case "warnings":
                for child in elt:
                    metars.warnings.append(child.text)
            case "time_taken_ms":
                metars.time_taken_ms = _parse_int(elt.text)
            case "data":
                metars_data.num_results = _parse_int(elt.attrib["num_results"])
                for child in elt:
                    metars_data.metars.append(_parse_metar(child))

    metars.data = metars_data
    return metars


def _parse_metar(metar_xml: ET.Element) -> Metar:
    metar = Metar()
    for elt in metar_xml:
        match elt.tag:
            case "raw_text":
                metar.raw_text = elt.text
            case "station_id":
                metar.station_id = elt.text
            case "observation_time":
                metar.observation_time_str = elt.text
                metar.observation_time = _parse_datetime(elt.text)
            case "latitude":
                metar.latitude = _parse_float(elt.text)
            case "longitude":
                metar.longitude = _parse_float(elt.text)
            case "temp_c":
                metar.temp_c = _parse_float(elt.text)
            case "dewpoint_c":
                metar.dewpoint_c = _parse_float(elt.text)
            case "wind_dir_degrees":
                metar.wind_dir_degrees = _parse_int(elt.text)
            case "wind_speed_kt":
                metar.wind_speed_kt = _parse_int(elt.text)
            case "wind_gust_kt":
                metar.wind_gust_kt = _parse_int(elt.text)
            case "visibility_statute_mi":
                metar.visibility_statute_mi = _parse_float(elt.text)
            case "altim_in_hg":
                metar.altim_in_hg = _parse_float(elt.text)
            case "sea_level_pressure_mb":
                metar.sea_level_pressure_mb = _parse_float(elt.text)
            case "quality_control_flags":
                metar.quality_control_flags = _parse_quality_control_flags(elt)
            case "sky_condition":
                metar.sky_conditions.append(_parse_sky_condition(elt))
            case "flight_category":
                metar.flight_category = elt.text
            case "three_hr_pressure_tendency_mb":
                metar.three_hr_pressure_tendency_mb = _parse_float(elt.text)
            case "maxT_c":
                metar.maxT_c = _parse_float(elt.text)
            case "minT_c":
                metar.minT_c = _parse_float(elt.text)
            case "maxT24hr_c":
                metar.maxT24hr_c = _parse_float(elt.text)
            case "minT24hr_c":
                metar.minT24hr_c = _parse_float(elt.text)
            case "precip_in":
                metar.precip_in = _parse_float(elt.text)
            case "pcp3hr_in":
                metar.pcp3hr_in = _parse_float(elt.text)
            case "pcp6hr_in":
                metar.pcp6hr_in = _parse_float(elt.text)
            case "pcp24hr_in":
                metar.pcp24hr_in = _parse_float(elt.text)
            case "snow_in":
                metar.snow_in = _parse_float(elt.text)
            case "vert_vis_ft":
                metar.vert_vis_ft = _parse_int(elt.text)
            case "metar_type":
                metar.metar_type = elt.text
            case "elevation_m":
                metar.elevation_m = _parse_float(elt.text)
    return metar


def _parse_quality_control_flags(qcf_xml: ET.Element) -> QualityControlFlag:
    qcf = QualityControlFlag()
    for child in qcf_xml:
        match child.tag:
            case "auto_station":
                qcf.auto_station = child.text
            case "maintenance_indicator_on":
                qcf.maintenance_indicator_on = child.text
    return qcf


def _parse_sky_condition(sky_condition_xml: ET.Element) -> SkyCondition:
    sky = SkyCondition()
    for key, value in sky_condition_xml.attrib.items():
        match key:
            case "sky_cover":
                sky.sky_cover = value
            case "cloud_base_ft_agl":
                sky.cloud_base_ft_agl = int(value)
    return sky


def _parse_int(int_str) -> Optional[int]:
    try:
        return int(int_str)
    except ValueError:
        return None


def _parse_float(float_str) -> Optional[float]:
    try:
        return float(float_str)
    except ValueError:
        return None


def _parse_datetime(datetime_str) -> Optional[datetime.datetime]:
    try:
        return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None
