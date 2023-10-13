import requests
import matplotlib.pyplot as plt


class Data:
    def __init__(self, frequency, country, indicator, startTime, endTime):
        self.database = "IFS"

        FREQ_FORMAT = ("A", "Q", "M")
        self.frequency = frequency  # FREQ
        if frequency not in FREQ_FORMAT:
            raise Exception("frequency format is not correct")

        self.country = country  # REF_AREA
        self.indicator = indicator  # INDICATOR
        self.startTime = startTime
        self.endTime = endTime

        self.raw_data = dict()
        self.data = list()
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
        url = f"{base}/{self.database}/{key}?startPeriod={self.startTime}&endPeriod={self.endTime}"
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
        """
        data: list = self.raw_data["CompactData"]["DataSet"]["Series"]["Obs"]
        for d in data:
            self.data.append({"time": d["@TIME_PERIOD"], "value": d["@OBS_VALUE"]})
        self.serialize_flag = True


class Series:
    def __init__(self):
        self.data_list = []

    def addData(self, data: Data):
        self.data_list.append(data)


country_code = "KR"

kr_gdp = Data("Q", country_code, "NGDP_SA_XDC", "1995", "2022")
# print(kr_gdp_data.getData())

kr_usd_rate = Data("Q", country_code, "ENDA_XDC_USD_RATE", "1995", "2022")
# print(kr_usd_rate.getData())

kr_policy_rate = Data("Q", country_code, "FPOLM_PA", "1995", "2022")
# print(kr_policy_rate.getData())


def plot_data():
    # 데이터 가공
    kr_gdp_data = kr_gdp.get_data()
    kr_usd_rate_data = kr_usd_rate.get_data()
    kr_policy_rate_data = kr_policy_rate.get_data()

    # 데이터 길이를 맞추기 위해 빈 데이터에 0 값 채우기
    max_length = max(len(kr_gdp_data), len(kr_usd_rate_data), len(kr_policy_rate_data))
    kr_gdp_data += [{"time": "", "value": "0"}] * (max_length - len(kr_gdp_data))
    kr_usd_rate_data += [{"time": "", "value": "0"}] * (
        max_length - len(kr_usd_rate_data)
    )
    kr_policy_rate_data += [{"time": "", "value": "0"}] * (
        max_length - len(kr_policy_rate_data)
    )

    times = [data["time"] for data in kr_gdp_data]
    gdp_values = [int(data["value"]) for data in kr_gdp_data]
    usd_rate_values = [float(data["value"]) for data in kr_usd_rate_data]
    policy_rate_values = [float(data["value"]) for data in kr_policy_rate_data]

    # 그래프 그리기
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 18))

    ax1.plot(times, gdp_values, marker="o", color="b", label="GDP Data")
    ax1.set_ylabel("GDP Value")
    ax1.set_title("Korea GDP Data")
    ax1.legend()

    ax2.plot(
        times, usd_rate_values, marker="o", color="g", label="USD Exchange Rate Data"
    )
    ax2.set_ylabel("Exchange Rate")
    ax2.set_title("Korea USD Exchange Rate Data")
    ax2.legend()

    ax3.plot(times, policy_rate_values, marker="o", color="r", label="Policy Rate Data")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Policy Rate")
    ax3.set_title("Korea Policy Rate Data")
    ax3.legend()

    plt.xticks(rotation=45)  # x축 라벨 회전
    plt.tight_layout()
    plt.show()


# 그래프 그리기 함수 호출
plot_data()
