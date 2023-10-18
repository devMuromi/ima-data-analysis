from data import Data


class Series:
    def __init__(self, title: str, start_year: int, end_year: int):
        self.title = title
        self.start_year = start_year
        self.end_year = end_year

        self.data_list: list(Data) = []

    def add_data(self, data: Data):
        self.data_list.append(data)
