from flask import Flask, render_template, request, url_for
import requests
from datetime import datetime, timedelta
import calendar
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
from flask import redirect
from PIL import Image


app = Flask(__name__)



@app.route('/')
def index():
    global response
    api_key = '219ee2cd1c341d93688001529dc36a06'
    city, _ = get_user_city()
    url = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=" + api_key
    print(url)
    response = requests.get(url).json()
    raingraph()
    forecast_list = response["list"]
    forecast_data = []
    index = 0
    while index < len(forecast_list):
        dt = forecast_list[index]['dt']
        temp = round(forecast_list[index]["main"]["temp"] - 273.15)
        desc = forecast_list[index]["weather"][0]["description"]
        icon = forecast_list[index]["weather"][0]["icon"]
        tempmin = round(forecast_list[index]["main"]["temp_min"] - 273.15)
        tempmax = round(forecast_list[index]["main"]["temp_max"] - 273.15)
        weather_data = forecast_list[index]["weather"]
        if "rain" in weather_data:
            precipitation = weather_data["rain"].get("3h", 0)
        else:
            precipitation = 0

        humidity = forecast_list[index]["main"]["humidity"]
        posted_day = datetime.fromtimestamp(dt).strftime("%A")
        posted_hour = datetime.fromtimestamp(dt).strftime("%H")
        posted_minute = datetime.fromtimestamp(dt).strftime("%M")
        if int(posted_hour) <= 11:
            posted_am_pm = "am"
        elif int(posted_hour) == 12:
            posted_am_pm = "pm"
        else:
            posted_am_pm = "pm"
            posted_hour = str(int(posted_hour) - 12)


        wind = forecast_list[index]['wind']['speed']





        index += 8
        dict = {
            "dt":dt,
            "temp":temp,
            "desc":desc,
            "icon": "http://openweathermap.org/img/w/" + icon + ".png",
            "tempmin":tempmin,
            "tempmax":tempmax,
            "precipitation":precipitation,
            "humidity":humidity,
            "wind":wind,
            "posted_day":posted_day,
            "posted_hour":posted_minute,
            "posted_minute":posted_minute,
            "posted_am_pm":posted_am_pm


        }

        forecast_data.append(dict)

        print(precipitation)

        print(posted_day)



    return render_template('home.html', forecast_data=forecast_data)



def get_user_city():
    print ('Get user city')
    try:
        response = requests.get('http://ip-api.com/json')
        data = response.json()
        city = data['city']
        country = data['country']
        return city, country
    except Exception as e:
        print("Error occurred while retrieving city:", e)
        return None


def tempgraph():
    global response
    print ('tempgraph')
    templist = {}
    for i in range(8):
        wind_dict[f"temptoday{i}"] = int(response['list']['main']['temp'] - 273.15)

    hour_data = (0, 3, 6, 9, 12, 15, 18, 21)

    pyplot.figure(figsize=(14, 3))
    pyplot.plot(hour_data, templist)
    pyplot.savefig("static/graph.png")
    print ('saved')

    image = Image.open('static/graph.png')
    crop_box = (130, 0, 1280, 300)
    cropped_image = image.crop(crop_box)
    cropped_image = cropped_image.convert('RGB')
    cropped_image.save('static/cropped_graph.png')


def raingraph():
    print ('raingraph')
    rainlist = {}
    for i in range(8):
        rain_dict[f"raintoday{i}"] = response["list"][i * 3].get("rain", {}).get("3h", 0) * 100


    hour_data = (0, 3, 6, 9, 12, 15, 18, 21)
    min_length = min(len(hour_data), len(rainlist))
    pyplot.figure(figsize=(14, 3))
    pyplot.plot(hour_data, rainlist)
    pyplot.savefig("static/raingraph.png")
    print ('should be saved')

    image = Image.open('static/raingraph.png')
    crop_box = (130, 0, 1280, 300)
    cropped_image = image.crop(crop_box)
    cropped_image = cropped_image.convert('RGB')
    cropped_image.save('static/cropped_raingraph.png')

def windgraph():
    print ('windgraph')
    wind_speeds = []
    for i in range(8):
        wind_speed = response['list'][i * 3]['wind']['speed']
        wind_speeds.append(wind_speed)

    hour_data = (0, 3, 6, 9, 12, 15, 18, 21)

    windlist = (windtoday, windtoday1, windtoday2, windtoday3, windtoday4, windtoday5, windtoday6, windtoday7)

    pyplot.figure(figsize=(14, 3))
    pyplot.plot(hour_data, windlist)
    pyplot.savefig("static/windgraph.png")

    image = Image.open('static/windgraph.png')
    crop_box = (130, 0, 1280, 300)
    cropped_image = image.crop(crop_box)
    cropped_image = cropped_image.convert('RGB')
    cropped_image.save('static/cropped_windgraph.png')














#hhhhhh



# @app.route('/results', methods=["POST", "GET"])
# def results():
#
#
#
#
#     first_weather_dict = weather_list[0]
#     description = first_weather_dict.get("weather", [{}])[0].get("description")
#     location = response.get('city', {}).get('name')
#     country = response.get('city', {}).get('country')
#     timezone = response.get('city', {}).get('timezone')
#     timestamp = first_weather_dict.get('dt')
#     date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
#     timestamp_local = datetime.fromtimestamp(timestamp)
#     temp_k = first_weather_dict.get("main", {}).get("temp")
#     temp_c = str(round(float(temp_k - 273.15), 1))
#     wind_speed = first_weather_dict.get("wind", {}).get("speed")
#     icon = first_weather_dict.get("weather", [{}])[0].get("icon")
#
#     today_date = datetime.now().date()
#     day0 = ("Today")
#
#
#     temptoday = [forecast['main']['temp'] for forecast in response.get("list", [])
#                         if datetime.fromtimestamp(forecast['dt']).date() == today_date]
#
#     temptoday = [forecast['main']['temp'] for forecast in response.get("list", [])
#                         if datetime.fromtimestamp(forecast['dt']).date() == today_date]
#     ttp1 = round(sum(temptoday) / len(temptoday) - 273.15)
#
#     tempmax = round(max(temptoday) - 273.15)
#     tempmin = round(min(temptoday) - 273.15)
#
#
#     temperaturelisttoday = [forecast['main']['temp'] for forecast in response.get("list", [])
#                         if datetime.fromtimestamp(forecast['dt']).date() == today_date]
#
#     print(temperaturelisttoday)
#
#
#
#
#     humiditytoday = response['list'][0]['main']['humidity']
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#     #today plus one temp
#     datetodayplusone = today_date + timedelta(days=1)
#     day1 = calendar.day_name[datetodayplusone.weekday()]
#     temptodayplusone = [forecast['main']['temp'] for forecast in response.get("list", [])
#                         if datetime.fromtimestamp(forecast['dt']).date() == datetodayplusone]
#     ttp1 = round(sum(temptodayplusone) / len(temptodayplusone) - 273.1)
#
#     tempmax1 = round(max(temptodayplusone) - 273.15)
#     tempmin1 = round(min(temptodayplusone) - 273.15)
#
#     day_one_icon = response['list'][0]['weather'][0]['icon']
#
#
#
#     #today plus 2 temp
#     datetodayplustwo = today_date + timedelta(days=2)
#     day2 = calendar.day_name[datetodayplustwo.weekday()]
#     temptodayplustwo = [forecast['main']['temp'] for forecast in weather_list
#                         if datetime.fromtimestamp(forecast['dt']).date() == datetodayplustwo]
#     ttp2 = round(sum(temptodayplustwo) / len(temptodayplustwo) - 273.15)
#     tempmax2 = round(max(temptodayplustwo) - 273.15)
#     tempmin2 = round(min(temptodayplustwo) - 273.15)
#
#     day_two_icon = response['list'][7]['weather'][0]['icon']
#
#
#     # today plus 3 temperature
#     datetodayplusthree = today_date + timedelta(days=3)
#     day3 = calendar.day_name[datetodayplusthree.weekday()]
#     temptodayplusthree = [forecast['main']['temp'] for forecast in weather_list
#                         if datetime.fromtimestamp(forecast['dt']).date() == datetodayplusthree]
#     ttp3 = round(sum(temptodayplusthree) / len(temptodayplusthree) - 273.1)
#     tempmax3 = round(max(temptodayplusthree) - 273.15)
#     tempmin3 = round(min(temptodayplusthree) - 273.15)
#
#     day_three_icon = response['list'][15]['weather'][0]['icon']
#
#
#     # today plus 4 temp
#     datetodayplusfour = today_date + timedelta(days=4)
#     day4 = calendar.day_name[datetodayplusfour.weekday()]
#     temptodayplusfour = [forecast['main']['temp'] for forecast in weather_list
#                         if datetime.fromtimestamp(forecast['dt']).date() == datetodayplusfour]
#     ttp4 = round(sum(temptodayplusfour) / len(temptodayplusfour) - 273.1)
#
#     tempmax4 = round(max(temptodayplusfour) - 273.15)
#     tempmin4 = round(min(temptodayplusfour) - 273.15)
#
#     day_four_icon = response['list'][23]['weather'][0]['icon']
#
#
#
#     #today plus 5 temp
#     datetodayplusfive = today_date + timedelta(days=5)
#     day5 = calendar.day_name[datetodayplusfive.weekday()]
#     temptodayplusfive = [forecast['main']['temp'] for forecast in weather_list
#                         if datetime.fromtimestamp(forecast['dt']).date() == datetodayplusfive]
#     ttp5 = round(sum(temptodayplusfive) / len(temptodayplusfive) - 273.1)
#
#     tempmax5 = round(max(temptodayplusfive) - 273.15)
#     tempmin5 = round(min(temptodayplusfive) - 273.15)
#     day_five_icon = response['list'][31]['weather'][0]['icon']
#
#
#
#
#
#
#     return render_template('results.html',city=city,humiditytoday=humiditytoday,
#                            preciptoday=preciptoday, temperaturelisttoday=temperaturelisttoday,
#                            day_date=day_data, temperature_data=temperature_data,
#                            day_one_icon=day_one_icon, day_two_icon=day_two_icon,
#                            day_three_icon=day_three_icon, day_four_icon=day_four_icon,
#                            day_five_icon=day_five_icon,  tempmax=tempmax, tempmin=tempmin,
#                            temptoday=temptoday, tempmin1=tempmin1, tempmin2=tempmin2,
#                            tempmin3=tempmin3, tempmin4=tempmin4, tempmin5=tempmin5,
#                            tempmax1=tempmax1, tempmax2=tempmax2, tempmax3=tempmax3,
#                            tempmax4=tempmax4, tempmax5=tempmax5, day0=day0, day1=day1,
#                            day2=day2, day3=day3, day4=day4, day5=day5, ttp1=ttp1,
#                            ttp2=ttp2, ttp3=ttp3, ttp4=ttp4, ttp5=ttp5, today_date=today_date, description=description,
#                            location=location,
#                            timezone=timezone, timestamp=timestamp, temp_c=temp_c, wind_speed=wind_speed, icon=icon,
#                            country=country, date=date, datetodayplusone=datetodayplusone,
#                            datetodayplustwo=datetodayplustwo, datetodayplusthree=datetodayplusthree,
#                            datetodayplusfour=datetodayplusfour, datetodayplusfive=datetodayplusfive)
#

if __name__ == '__main__':
    app.run(debug=True)
