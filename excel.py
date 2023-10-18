from data import Data, Frequency
from series import Series
from openpyxl import Workbook
import datetime


class Excel(Series):
    def __init__(
        self,
        title: str,
        start_year: int,
        end_year: int,
        frequency: Frequency = Frequency.F,
    ):
        super().__init__(title, start_year, end_year)

        if frequency not in ["A", "Q", "M", "F"]:
            raise Exception("frequency format is not correct")
        self.frequency = frequency

    def create_excel(self):
        wb = Workbook()
        ws = wb.active
        for data in self.data_list:
            freq: Frequency = self.frequency
            if freq == Frequency.F:
                freq = data.frequency
            time = [
                "time:" + freq,
            ]
            for t in data.get_convert_data(self.frequency)["time"]:
                time.append(Data.convert_time(t, freq))
            ws.append(time)

            value = [data.get_title()]
            value.extend(data.get_convert_data(self.frequency)["value"])
            ws.append(value)
            ws.append([])

        now = datetime.datetime.now()
        wb.save(self.title + now.strftime("_%y%m%d_%H%M") + ".xlsx")
