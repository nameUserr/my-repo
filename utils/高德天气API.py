import requests
import json
import pandas as pd

url = "https://restapi.amap.com/v3/weather/weatherInfo?key=304c170a04218cf71a75e77a77e4d00f&extensions=base&output=json"
citys = ['110101','110102','110105','110106']
city_infos = []
for city in citys:
    url1 = url + "&city=" + city
    response = requests.get(url1)
    city_info = json.loads(response.text)["lives"][0]
    city_infos.append(city_info)
for city in city_infos:
    print(city)

df = pd.DataFrame(data = city_infos)
print(df)
df.to_excel("city_info.xlsx")