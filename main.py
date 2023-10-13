import requests
import matplotlib.pyplot as plt


class Data:
    def __init__(
        self,
        title: str,
        frequency,
        country: str,
        indicator: str,
        start_time: int,
        end_time: int,
    ):
        self.database = "IFS"
        self.title = title

        FREQ_FORMAT = ("A", "Q", "M")
        self.frequency = frequency  # FREQ
        if frequency not in FREQ_FORMAT:
            raise Exception("frequency format is not correct")

        self.country = country  # REF_AREA
        self.indicator = indicator  # INDICATOR
        self.start_time = start_time
        self.end_time = end_time

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
        url = f"{base}/{self.database}/{key}?startPeriod={self.start_time}&endPeriod={self.end_time}"
        return url

    def _query(self) -> None:
        """
        update raw_data
        """
        res = requests.get(self._create_url())
        self.raw_data = res.json()

    def _serialize(self) -> None:
        """
        update data
        TIME_PERIOD: 2010, 2010-Q1, 2010-01
        """
        data: list = self.raw_data["CompactData"]["DataSet"]["Series"]["Obs"]

        for d in data:
            if "@TIME_PERIOD" not in d or "@OBS_VALUE" not in d:
                continue
            if self.frequency == "M":
                self.data["value"].append(float(d["@OBS_VALUE"]))
                self.data["time"].append(d["@TIME_PERIOD"])
            elif self.frequency == "Q":
                for i in range(2, -1, -1):
                    self.data["value"].append(float(d["@OBS_VALUE"]))
                    self.data["time"].append(
                        d["@TIME_PERIOD"][0:5]
                        + str(int(d["@TIME_PERIOD"][6:7]) * 3 - i)
                    )

        self.serialize_flag = True

    def get_x_range(self) -> int:
        return self.end_time - self.start_time + 1

    def get_title(self) -> str:
        return self.title


class Series:
    def __init__(self):
        self.data_list = []

    def add_data(self, data: Data):
        self.data_list.append(data)

    def draw_graph(self):
        pass


# japan_series = Series()
# japan_series.add_data(Data("Japan GDP", "Q", "JP", "NGDP_SA_XDC", "1995", "2022"))
# japan_series.add_data(Data("Japan GDP", "Q", "JP", "ENDA_XDC_USD_RATE", "1995", "2022"))
# japan_series.add_data(Data("Japan GDP", "Q", "JP", "FPOLM_PA", "1995", "2022"))


JAPAN_CODE = "JP"
START_YEAR = 1995
END_YEAR = 2022
kr_gdp = Data("Japan GDP", "Q", JAPAN_CODE, "NGDP_SA_XDC", START_YEAR, END_YEAR)
# print(kr_gdp_data.getData())

kr_usd_rate = Data(
    "Japan USD rate", "Q", JAPAN_CODE, "ENDA_XDC_USD_RATE", START_YEAR, END_YEAR
)
# print(kr_usd_rate.getData())

kr_policy_rate = Data(
    "Japan policy rate", "Q", JAPAN_CODE, "FPOLM_PA", START_YEAR, END_YEAR
)
# print(kr_policy_rate.getData())


def plot_data():
    # 데이터 가공
    kr_gdp_data = kr_gdp.get_data()
    kr_usd_rate_data = kr_usd_rate.get_data()
    kr_policy_rate_data = kr_policy_rate.get_data()

    # time_list = [data["time"] for data in kr_gdp_data]
    # value_list = [data["value"] for data in kr_gdp_data]

    # plt.plot(time_list, value_list, label=kr_gdp.get_title())
    plt.subplot(3, 1, 1)
    plt.plot("time", "value", data=kr_gdp.get_data(), label=kr_gdp.get_title())
    plt.ylabel(kr_gdp.get_title())
    plt.xlabel("Time")
    plt.xticks(["1995-1", "2000-1", "2005-1", "2010-1", "2015-1", "2020-1"])

    plt.subplot(3, 1, 2)
    plt.plot(
        "time", "value", data=kr_usd_rate.get_data(), label=kr_usd_rate.get_title()
    )
    plt.ylabel(kr_usd_rate.get_title())
    plt.xlabel("Time")
    plt.xticks(["1995-1", "2000-1", "2005-1", "2010-1", "2015-1", "2020-1"])

    plt.subplot(3, 1, 3)
    plt.plot(
        "time",
        "value",
        data=kr_policy_rate.get_data(),
        label=kr_policy_rate.get_title(),
    )
    plt.ylabel(kr_policy_rate.get_title())
    plt.xlabel("Time")
    plt.xticks(["1995-1", "2000-1", "2005-1", "2010-1", "2015-1", "2020-1"])

    plt.show()

    # # 데이터 길이를 맞추기 위해 빈 데이터에 0 값 채우기
    # max_length = max(len(kr_gdp_data), len(kr_usd_rate_data), len(kr_policy_rate_data))
    # kr_gdp_data += [{"time": "", "value": "0"}] * (max_length - len(kr_gdp_data))
    # kr_usd_rate_data += [{"time": "", "value": "0"}] * (
    #     max_length - len(kr_usd_rate_data)
    # )
    # kr_policy_rate_data += [{"time": "", "value": "0"}] * (
    #     max_length - len(kr_policy_rate_data)
    # )

    # times = [data["time"] for data in kr_gdp_data]
    # gdp_values = [int(data["value"]) for data in kr_gdp_data]
    # usd_rate_values = [float(data["value"]) for data in kr_usd_rate_data]
    # policy_rate_values = [float(data["value"]) for data in kr_policy_rate_data]

    # # 그래프 그리기
    # fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 18))

    # ax1.plot(times, gdp_values, marker="o", color="b", label="GDP Data")
    # ax1.set_ylabel("GDP Value")
    # ax1.set_title("Korea GDP Data")
    # ax1.legend()

    # ax2.plot(
    #     times, usd_rate_values, marker="o", color="g", label="USD Exchange Rate Data"
    # )
    # ax2.set_ylabel("Exchange Rate")
    # ax2.set_title("Korea USD Exchange Rate Data")
    # ax2.legend()

    # ax3.plot(times, policy_rate_values, marker="o", color="r", label="Policy Rate Data")
    # ax3.set_xlabel("Time")
    # ax3.set_ylabel("Policy Rate")
    # ax3.set_title("Korea Policy Rate Data")
    # ax3.legend()

    # plt.xticks(rotation=45)  # x축 라벨 회전
    # plt.tight_layout()
    # plt.show()


# 그래프 그리기 함수 호출
plot_data()
