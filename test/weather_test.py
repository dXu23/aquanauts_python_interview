from pytest import fixture

from interview import weather
from filecmp import cmp
import io

def test_returns_just_fields_if_data_empty():
    reader = io.StringIO("")
    writer = io.StringIO()
    weather.process_csv(reader, writer)
    assert writer.getvalue() == "Station Name,Date,Min Temp,Max Temp,First Temp,Last Temp\n"

def test_just_one_station():
    with open("data/one_station.csv") as one_station_input, open("data/one_station_expected.csv") as one_station_expected:
        one_station_actual = io.StringIO()
        weather.process_csv(one_station_input, one_station_actual)
        # print(one_station_actual.getvalue())
        assert one_station_actual.getvalue() == one_station_expected.read()

def test_multiple_stations():
    with open("data/multiple_stations.csv") as multiple_stations_input, open("data/multiple_stations_expected.csv") as multiple_stations_expected:
        multiple_stations_actual = io.StringIO()
        weather.process_csv(multiple_stations_input, multiple_stations_actual)
        # print(multiple_stations_actual.getvalue())
        assert multiple_stations_actual.getvalue() == multiple_stations_expected.read()

