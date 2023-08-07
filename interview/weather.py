import csv
from datetime import datetime
from typing import TextIO

class TemperatureData:
    def __init__(self, minTemp: float, maxTemp: float, firstHour: int, firstTemp: float, lastHour: int, lastTemp: float):
        """
        Constructs all attributes for an instance of TemperatureData, which
        represents the aggregate data for a weather station on a particular day

        param: minTemp float: minimum temperature
        param: maxTemp float: maximum temperature
        param: firstHour int: earliest hour at which a temperature was recorded
        param: firstTemp int: earliest temperature
        param: lastHour int: latest hour at which a temperature was recorded
        param: lastTemp int: latest temperature
        """
        self.__minTemp = minTemp
        self.__maxTemp = maxTemp
        self.__firstHour = firstHour
        self.__firstTemp = firstTemp
        self.__lastHour = lastHour
        self.__lastTemp = lastTemp

    def updateFirstTemp(self, newHour: int, newTemp: float) -> None:
        """
        Updates the earliest temperature if the corresponding hour is
        earlier than the existing earliest hour.

        param: newHour int: hour that temperature was recorded at
        param: newTemp float: temperature
        """
        if newHour < self.__firstHour:
            self.__firstHour = newHour
            self.__firstTemp = newTemp

    def updateLastTemp(self, newHour: int, newTemp: float) -> None:
        """
        Updates the temperature if the corresponding hour is later
        than the existing latest hour.

        param: newHour int: hour that temperature was recorded at
        param: newTemp float: temperature
        """
        if newHour > self.__lastHour:
            self.__lastHour = newHour
            self.__lastTemp = newTemp

    def updateMinTemp(self, newTemp: float):
        """
        Updates the current minimum temperature if newTemp is less.

        param: newTemp float: temperature to update to if it is less than existing minTemp
        """
        self.__minTemp = min(self.__minTemp, newTemp)

    def updateMaxTemp(self, maxTemp: float):
        """
        Updates the current maximum temperature if newTemp is greater.

        param: newTemp float: temperature to update to it is greater than existing minTemp
        """
        self.__maxTemp = max(self.__maxTemp, maxTemp)

    def output(self) -> list[str]:
        """
        Returns a list suitable as input for csvwriter.writerow

        returns: list containing minimum temperature, maximum temperature, first
        temperature, and last temperature
        """
        return [
            str(self.__minTemp),
            str(self.__maxTemp),
            str(self.__firstTemp),
            str(self.__lastTemp)
        ]

    def __repr__(self) -> str:
        """
        Returns a string containing all the temperature data. For debugging purposes only.

        returns: string containing minimum temperature, maximum temperature, earliest temperature, and latest temperature
        """
        return f"TemperatureData(minTemp, maxTemp, firstTemp, lastTemp): ({self.__minTemp}, {self.__maxTemp}, {self.__firstTemp}, {self.__lastTemp})"

def process_csv(reader: TextIO, writer: TextIO) -> None:
    """
    Reads CSV containing weather data and writes aggregate data like minimum temperature,
    maximum temperature, earliest temperature, and latest temperature of different weather
    stations on different dates to a CSV file object.

    param: reader (TextIO): CSV file object containing weather to read lines from.
    param: writer (TextIO): CSV file object to write aggregates of weather data to
    """

    FIELDS = ["Station Name", "Date", "Min Temp", "Max Temp", "First Temp", "Last Temp"]

    # stationDateDict is a dictionary of dicts, with the first key being station and second key being date as string
    stationDateDict = {}

    csvReader = csv.DictReader(reader)
    csvWriter = csv.writer(writer, lineterminator = "\n")

    for row in csvReader:
        station = row["Station Name"]

        try:
            date = datetime.strptime(row["Measurement Timestamp"], "%m/%d/%Y %I:%M:%S %p")
            temperature = float(row["Air Temperature"])
        except Exception as exp:
            raise ValueError(str(exp))

        hour = date.hour
        outputDate = date.strftime("%m/%d/%Y")

        if station not in stationDateDict:
            stationDateDict[station] = { outputDate: TemperatureData(temperature, temperature, hour, temperature, hour, temperature) }
        else:
            if outputDate not in stationDateDict[station]:
                stationDateDict[station][outputDate] = TemperatureData(temperature, temperature, hour, temperature, hour, temperature)
            else:
                stationDateDict[station][outputDate].updateFirstTemp(hour, temperature)
                stationDateDict[station][outputDate].updateLastTemp(hour, temperature)
                stationDateDict[station][outputDate].updateMinTemp(temperature)
                stationDateDict[station][outputDate].updateMaxTemp(temperature)

    csvWriter.writerow(FIELDS)
    for station, dateTempData in stationDateDict.items():
        for date, tempData in dateTempData.items():
            csvWriter.writerow([station, date] + tempData.output())


