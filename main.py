import requests
import matplotlib.pyplot as plt


# https://datahelp.imf.org/knowledgebase/articles/1968408-how-to-use-the-api-python-and-r
class Data:
    def __init__(
        self,
        title: str,
        frequency,
        country: str,
        indicator: str,
        start_year: int,
        end_year: int,
    ):
        self.database: str = "IFS"
        self.title: str = title

        FREQ_FORMAT = ("A", "Q", "M")
        self.frequency = frequency  # FREQ
        if frequency not in FREQ_FORMAT:
            raise Exception("frequency format is not correct")

        self.country: str = country  # REF_AREA
        self.indicator: str = indicator  # INDICATOR
        self.start_year: int = start_year
        self.end_year: int = end_year

        self.raw_data = dict()
        self.data = {"time": [], "value": []}
        self.serialize_flag = False

        self._query()
        self._serialize()

    def get_data(self):
        if self.serialize_flag == False:
            raise Exception("data is not serialized. please call serialize method")
        return self.data

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
        update data
        TIME_PERIOD: 2010, 2010-Q1, 2010-01
        """
        try:
            data: list = self.raw_data["CompactData"]["DataSet"]["Series"]["Obs"]
        except:
            print(self.raw_data)
            raise Exception("data is not correct format. Frequency may be unable")

        for d in data:
            if "@TIME_PERIOD" not in d or "@OBS_VALUE" not in d:
                continue
            if self.frequency == "M":
                self.data["value"].append(float(d["@OBS_VALUE"]))
                time_data: list(str) = d["@TIME_PERIOD"].split("-")
                self.data["time"].append(int(time_data[0]) * 12 + int(time_data[1]) - 1)
            elif self.frequency == "Q":
                for i in range(-3, 0):
                    self.data["value"].append(float(d["@OBS_VALUE"]))
                    time_data: list(str) = d["@TIME_PERIOD"].split("-Q")
                    self.data["time"].append(
                        int(time_data[0]) * 12 + int(time_data[1]) * 3 + i
                    )
            elif self.frequency == "A":
                for i in range(12):
                    self.data["value"].append(float(d["@OBS_VALUE"]))
                    self.data["time"].append(int(d["@TIME_PERIOD"]) * 12 + i)
            # 이전 str 방식
            # if self.frequency == "M":
            #     self.data["value"].append(float(d["@OBS_VALUE"]))
            #     self.data["time"].append(d["@TIME_PERIOD"])
            # elif self.frequency == "Q":
            #     for i in range(2, -1, -1):
            #         self.data["value"].append(float(d["@OBS_VALUE"]))
            #         self.data["time"].append(
            #             d["@TIME_PERIOD"][0:5]
            #             + str(int(d["@TIME_PERIOD"][6:7]) * 3 - i)
            #         )
            # elif self.frequency == "A":
            #     for i in range(1, 13):
            #         self.data["value"].append(float(d["@OBS_VALUE"]))
            #         self.data["time"].append(d["@TIME_PERIOD"][0:4] + "-" + str(i))

        self.serialize_flag = True

    def get_x_range(self) -> int:
        return self.end_year - self.start_year + 1

    def get_title(self) -> str:
        return self.title


class Series:
    def __init__(self, title: str, start_year: int, end_year: int, interval=1):
        self.title = title
        self.start_year = start_year
        self.end_year = end_year
        if interval <= 0:
            raise Exception("interval must be positive")
        self.interval = interval

        self.data_list: list(Data) = []

        self.x_raw_year: list(int) = []
        self.x_year: list(str) = []
        for i in range(start_year, end_year + 1, interval):
            self.x_raw_year.append(i * 12)
            self.x_year.append(str(i) + "-1")

    def add_data(self, data: Data):
        self.data_list.append(data)

    def draw_graph(self):
        plt.title(self.title)
        plt.yticks([])  # y축 눈금 제거
        plt.xticks([])  # x축 눈금 제거
        for i in range(len(self.data_list)):
            data = self.data_list[i]

            plt.subplot(len(self.data_list), 1, i + 1)
            plt.plot("time", "value", data=data.get_data(), label=data.get_title())
            plt.ylabel(data.get_title())
            plt.xlabel("Time")
            plt.xlim(self.start_year * 12, self.end_year * 12)
            plt.xticks(self.x_raw_year, labels=self.x_year)
            plt.grid(True)

        plt.show()


##### KOREA #####
COUTRY_CODE = "KR"
START_YEAR = 1995
END_YEAR = 2022
series = Series("Korea Data", START_YEAR, END_YEAR)
series.add_data(
    Data("Korea GDP", "Q", COUTRY_CODE, "NGDP_SA_XDC", START_YEAR, END_YEAR)
)
series.add_data(
    Data("Korea USD rate", "Q", COUTRY_CODE, "ENDA_XDC_USD_RATE", START_YEAR, END_YEAR)
)
series.add_data(
    Data("Korea policy rate", "Q", COUTRY_CODE, "FPOLM_PA", START_YEAR, END_YEAR)
)
series.draw_graph()


##### JAPAN #####
COUTRY_CODE = "JP"
START_YEAR = 1995
END_YEAR = 2022
japan_series = Series("Japan Data", START_YEAR, END_YEAR)
japan_series.add_data(
    Data("Japan GDP", "Q", COUTRY_CODE, "NGDP_SA_XDC", START_YEAR, END_YEAR)
)
japan_series.add_data(
    Data("Japan USD rate", "Q", COUTRY_CODE, "ENDA_XDC_USD_RATE", START_YEAR, END_YEAR)
)
japan_series.add_data(
    Data("Japan policy rate", "Q", COUTRY_CODE, "FPOLM_PA", START_YEAR, END_YEAR)
)
japan_series.draw_graph()
