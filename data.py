import requests
import enum
from StrEnum import StrEnum


class Frequency(StrEnum):
    A = enum.auto()  # annual
    Q = enum.auto()  # quarterly
    M = enum.auto()  # monthly
    F = enum.auto()  # free


class ConvertType(StrEnum):
    Average = enum.auto()
    Sum = enum.auto()
    # Max = enum.auto()
    # Min = enum.auto()


class Data:
    def __init__(
        self,
        title: str,
        frequency: Frequency,
        country: str,
        indicator: str,
        start_year: int,
        end_year: int,
        convert_type: ConvertType = ConvertType.Average,
    ):
        self.database: str = "IFS"

        self.title: str = title

        if frequency not in Frequency.__members__:
            raise Exception("frequency format is not correct")
        self.frequency = frequency  # FREQ

        self.country: str = country  # REF_AREA
        self.indicator: str = indicator  # INDICATOR
        self.start_year: int = start_year
        self.end_year: int = end_year
        self.convert_type = convert_type

        self.raw_data = dict()
        self.data = {"time": [], "value": []}
        self.serialize_flag = False
        self.annual_data = {"time": [], "value": []}
        self.annual_data_flag = False
        self.quarterly_data = {"time": [], "value": []}
        self.quarterly_data_flag = False
        self.monthly_data = {"time": [], "value": []}
        self.monthly_data_flag = False

        self._query()
        self._serialize()

    def get_title(self) -> str:
        return self.title

    def get_data(self) -> dict:
        if self.serialize_flag == False:
            raise Exception("data is not serialized. please call serialize method")
        return self.data

    def get_convert_data(self, frequency: Frequency) -> dict:
        if frequency == Frequency.A:
            if self.annual_data_flag == False:
                self._convert_annual_data()
            return self.annual_data
        if frequency == Frequency.Q:
            if self.quarterly_data_flag == False:
                self._convert_quarterly_data()
            return self.quarterly_data
        if frequency == Frequency.M:
            if self.monthly_data_flag == False:
                self._convert_monthly_data()
            return self.monthly_data
        if frequency == Frequency.F:
            return self.get_data()

    def convert_time(time: int, frequency: Frequency) -> str:
        if frequency == Frequency.A:
            return str(time)
        if frequency == Frequency.Q:
            return Data.convert_quartely_time(time)
        if frequency == Frequency.M:
            return Data.convert_monthly_time(time)

    def convert_quartely_time(time: int) -> str:
        return f"{time // 4}-Q{time % 4 + 1}"

    def convert_monthly_time(time: int) -> str:
        return f"{time // 12}-{time % 12 + 1}"

    def _convert_value(self, values: list, ret_size: int) -> list:
        if self.convert_type == ConvertType.Average:
            # monthly 금리 라면 평균 내서 annual data로 변환
            # annual 금리 라면 평균 내서 monthly data로 변환
            return [float(sum(values)) / len(values) for _ in range(ret_size)]
        if self.convert_type == ConvertType.Sum:
            # monthly GDP data라면 합해서 annual data로 변환
            # annual GDP data라면 나눠서(/12) monthly data로 변환
            return [float(sum(values)) / ret_size for _ in range(ret_size)]

    def _convert_annual_data(self) -> None:
        if self.frequency == "A":
            self.annual_data = self.get_data()
        # elif self.frequency == "Q":
        #     for d in self.get_data():
        #         for i in range(4):
        #             self.annual_data["value"].append(d["value"])
        #             self.annual_data["time"].append(d["time"] + i)

        self.annual_data_flag = True

    def _convert_quarterly_data(self) -> None:
        if self.frequency == "A":
            for i in range(len(self.get_data()["time"])):
                self.quarterly_data["value"].extend(
                    self._convert_value([self.get_data()["value"][i]], 4)
                )
                self.quarterly_data["time"].extend(
                    [self.get_data()["time"][i] * 4 + j for j in range(4)]
                )
        elif self.frequency == "Q":
            self.quarterly_data = self.get_data()
        elif self.frequency == "M":
            for t in range(self.start_year * 4, self.end_year * 4 + 4):
                count = 0
                values = []
                for i in range(3):
                    if t * 3 + i in self.data["time"]:
                        count += 1
                        values.append(
                            self.data["value"][self.data["time"].index(t * 3 + i)]
                        )
                if count == 0:
                    continue
                self.quarterly_data["time"].append(t)
                self.quarterly_data["value"].extend(self._convert_value(values, 1))

    def _convert_monthly_data(self):
        if self.frequency == "A":
            for i in range(len(self.get_data()["time"])):
                self.monthly_data["value"].extend(
                    self._convert_value([self.get_data()["value"][i]], 12)
                )
                self.monthly_data["time"].extend(
                    [self.get_data()["time"][i] * 4 + j for j in range(12)]
                )
        elif self.frequency == "Q":
            for i in range(len(self.get_data()["time"])):
                self.monthly_data["value"].extend(
                    self._convert_value([self.get_data()["value"][i]], 3)
                )
                self.monthly_data["time"].extend(
                    [self.get_data()["time"][i] * 4 + j for j in range(3)]
                )
        elif self.frequency == "M":
            self.monthly_data = self.get_data()

    def _create_url(self) -> str:
        """
        In general, for setting up your query, the root of the URL that you want to retrieve data from is:  http://dataservices.imf.org/REST/SDMX_XML.svc/

        Following that root, you will need to add on additional details about what data you would like:

        Data type: "CompactData" to retrieve data, "DataStructure" to retrieve series information, or "GenericMetadata" to get metadata.
        Database you would like to query: For example, International Financial Statistics ("IFS"), Balance of Payments ("BOP"), etc.
        Frequency: Annual ("A"), Quarterly ("Q"), Monthly ("M")
        Specific Indicator interested in: For CPI this is " PCPI_IX"

        So, if you want to query the IFS database for monthly CPI data for 2000-2001, you would want to use the URL:
            http://dataservices.imf.org/REST/SDMX_XML.svc/CompactData/IFS/M..PCPI_IX.?startPeriod=2000&endPeriod=2001
        """
        base = "http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData"
        key = f"{self.frequency}.{self.country}.{self.indicator}."
        url = f"{base}/{self.database}/{key}?startPeriod={self.start_year}&endPeriod={self.end_year}"
        return url

    def _query(self) -> None:
        """
        update raw_data
        """
        res = requests.get(self._create_url())
        try:
            self.raw_data = res.json()
        except:
            print(res.text)
            raise Exception("data is not json format")

    def _serialize(self) -> None:
        """
        TIME_PERIOD: 2010, 2010-Q1, 2010-01
        time data format:
        if annual: year
        if quarterly: year * 4 + quarter - 1
        if monthly: year * 12 + month - 1
        """
        try:
            data: list = self.raw_data["CompactData"]["DataSet"]["Series"]["Obs"]
        except:
            print(self.raw_data)
            raise Exception("data is not correct format. Frequency may be unable")

        for d in data:
            if "@TIME_PERIOD" not in d or "@OBS_VALUE" not in d:
                continue
            self.data["value"].append(float(d["@OBS_VALUE"]))
            if self.frequency == "M":
                time_data: list(str) = d["@TIME_PERIOD"].split("-")
                self.data["time"].append(int(time_data[0]) * 12 + int(time_data[1]) - 1)
            elif self.frequency == "Q":
                time_data: list(str) = d["@TIME_PERIOD"].split("-Q")
                self.data["time"].append(int(time_data[0]) * 4 + int(time_data[1]) - 1)
            elif self.frequency == "A":
                self.data["time"].append(int(d["@TIME_PERIOD"]))

        self.serialize_flag = True
