import requests
import time
from datetime import datetime
import config
import SaveData


def getData():
    AllData = {}
    for city in config.CITY:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.API_KEY}&units=metric"
        response = requests.get(url)
        jsonResponse = response.json() 
        output = {}
        curr_datetime = datetime.fromtimestamp(jsonResponse['dt'])
        main_feel = jsonResponse['weather'][0]['main']
        temperature = jsonResponse['main']['temp'] 
        feels_like = jsonResponse['main']['feels_like']
        output['date_time'] = curr_datetime
        output["main"] = main_feel
        output["temperature"] = temperature
        output["feels_like"] = feels_like
        AllData[f"{city}"] = output
    return AllData


if __name__ == "__main__":
    while(True):
        output = getData()
        for city, attributes in output.items():
            SaveData.write_city_data(city, attributes)
        time.sleep(config.TIMESTAMP)
