import requests

response = requests.get(
    "http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/IFS/Q.KR.NGDP_SA_XDC.?startPeriod=1995&endPeriod=2022"
)

# print(response.json())
print(type(response.json()))

data = response.json()

import matplotlib.pyplot as plt

obs_values = data["CompactData"]["DataSet"]["Series"]["Obs"]
x = [obs["@TIME_PERIOD"] for obs in obs_values]
y = [int(obs["@OBS_VALUE"]) for obs in obs_values]

plt.figure(figsize=(10, 6))
plt.plot(x, y, marker="o", linestyle="-", color="b", label="OBS_VALUE")
plt.xlabel("시간")
plt.ylabel("OBS_VALUE")
plt.title("시간에 따른 OBS_VALUE 그래프")
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend()
plt.show()
