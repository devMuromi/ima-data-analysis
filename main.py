from data import Data
from graph import Graph
from excel import Excel

# https://datahelp.imf.org/knowledgebase/articles/1968408-how-to-use-the-api-python-and-r
# https://data.imf.org/

##### KOREA #####
# COUTRY_CODE = "KR"
# START_YEAR = 1995
# END_YEAR = 2022
# series = Graph("Korea Data", START_YEAR, END_YEAR, "Q", 6)
# series.add_data(
#     Data("Korea GDP", "Q", COUTRY_CODE, "NGDP_SA_XDC", START_YEAR, END_YEAR, "Sum")
# )
# series.add_data(
#     Data("Korea USD rate", "Q", COUTRY_CODE, "ENDA_XDC_USD_RATE", START_YEAR, END_YEAR)
# )
# series.add_data(
#     Data("Korea policy rate", "Q", COUTRY_CODE, "FPOLM_PA", START_YEAR, END_YEAR)
# )
# series.draw_graph()

##### Excel #####
COUTRY_CODE = "KR"
START_YEAR = 1995
END_YEAR = 2022
series = Excel("Korea Data", START_YEAR, END_YEAR, "M")
series.add_data(
    Data("Korea GDP", "Q", COUTRY_CODE, "NGDP_SA_XDC", START_YEAR, END_YEAR, "Sum")
)
series.add_data(
    Data("Korea USD rate", "Q", COUTRY_CODE, "ENDA_XDC_USD_RATE", START_YEAR, END_YEAR)
)
series.add_data(
    Data("Korea policy rate", "Q", COUTRY_CODE, "FPOLM_PA", START_YEAR, END_YEAR)
)
series.create_excel()
print("엑셀 출력 완료")


##### JAPAN #####
# COUTRY_CODE = "JP"
# START_YEAR = 1995
# END_YEAR = 2022
# japan_series = Series("Japan Data", START_YEAR, END_YEAR)
# japan_series.add_data(
#     Data("Japan GDP", "Q", COUTRY_CODE, "NGDP_SA_XDC", START_YEAR, END_YEAR)
# )
# japan_series.add_data(
#     Data("Japan USD rate", "Q", COUTRY_CODE, "ENDA_XDC_USD_RATE", START_YEAR, END_YEAR)
# )
# japan_series.add_data(
#     Data("Japan policy rate", "Q", COUTRY_CODE, "FPOLM_PA", START_YEAR, END_YEAR)
# )
# japan_series.draw_graph()


##### VIETNAM #####
# COUTRY_CODE = "VN"
# START_YEAR = 1995
# END_YEAR = 2022
# series = Graph("Vietnam Data", START_YEAR, END_YEAR, "A", 1)
# series.add_data(
#     Data("Vietnam GDP", "A", COUTRY_CODE, "NGDP_XDC", START_YEAR, END_YEAR, "Sum")
# )
# series.add_data(
#     Data(
#         "Vietnam USD rate", "M", COUTRY_CODE, "ENDA_XDC_USD_RATE", START_YEAR, END_YEAR
#     )
# )
# series.add_data(
#     Data("Vietnam policy rate", "Q", COUTRY_CODE, "FPOLM_PA", START_YEAR, END_YEAR)
# )
# series.draw_graph()
