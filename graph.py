from series import Series
from data import Frequency, Data
import matplotlib.pyplot as plt


class Graph(Series):
    def __init__(
        self,
        title: str,
        start_year: int,
        end_year: int,
        frequency: Frequency = Frequency.Q,
        interval: int = 1,
    ):
        super().__init__(title, start_year, end_year)
        self.frequency = frequency
        if interval <= 0:
            raise Exception("interval must be positive")
        self.interval = interval

        self.x_raw_year: list(int) = []
        self.x_year: list(str) = []

        if self.frequency == "A":
            for i in range(start_year, end_year + 1, interval):
                self.x_raw_year.append(i)
                self.x_year.append(Data.convert_annual_time(i))
        elif self.frequency == "Q":
            for i in range(start_year * 4, end_year * 4 + 1, interval):
                self.x_raw_year.append(i)
                self.x_year.append(Data.convert_quartely_time(i))
        elif self.frequency == "M":
            for i in range(start_year * 12, end_year * 12 + 1, interval):
                self.x_raw_year.append(i)
                self.x_year.append(Data.convert_monthly_time(i))

    def draw_graph(self):
        plt.title(self.title)
        plt.yticks([])  # y축 눈금 제거
        plt.xticks([])  # x축 눈금 제거
        for i in range(len(self.data_list)):
            data = self.data_list[i]

            plt.subplot(len(self.data_list), 1, i + 1)
            if self.frequency == "A":
                plt.plot(
                    "time", "value", data=data.get_annual_data(), label=data.get_title()
                )
            elif self.frequency == "Q":
                plt.plot(
                    "time",
                    "value",
                    data=data.get_quarterly_data(),
                    label=data.get_title(),
                )
            elif self.frequency == "M":
                plt.plot(
                    "time",
                    "value",
                    data=data.get_monthly_data(),
                    label=data.get_title(),
                )
            plt.ylabel(data.get_title())
            plt.xlabel("Time")
            if self.frequency == "A":
                plt.xlim(self.start_year, self.end_year)
            elif self.frequency == "Q":
                plt.xlim(self.start_year * 4, self.end_year * 4 + 3)
            elif self.frequency == "M":
                plt.xlim(self.start_year * 12, self.end_year * 12 + 11)
            plt.xticks(self.x_raw_year, labels=self.x_year)
            plt.grid(True)

        plt.show()
