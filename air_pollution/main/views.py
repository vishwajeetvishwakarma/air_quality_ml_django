from django.shortcuts import render
import requests
import pandas as pd
import plotly.express as px
import plotly.offline as plot
import json
from django.templatetags.static import static

header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def get_data(url):
    r = requests.get(url, headers=header)
    df = pd.read_html(r.text)
    return df[0]


mumbai_areas = ["Andheri", "Bandra", "Borivali", "Chembur", "Colaba", "Dadar", "Dharavi", "Goregaon", "Juhu", "Kandivali",
                "Khar", "Malad", "Mira Road", "Mulund", "Navi Mumbai", "Powai", "Santacruz", "Thane", "Vashi", "Virar", "Worli"]


def get_mumbai_date():
    mumbai = pd.DataFrame()
    for i in mumbai_areas:
        url = "https://air-quality-by-api-ninjas.p.rapidapi.com/v1/airquality"
        querystring = {"city": i}
        headers = {
            "X-RapidAPI-Key": "5b83c84710msh3a7606480232177p15f25fjsnbf34847814ce",
            "X-RapidAPI-Host": "air-quality-by-api-ninjas.p.rapidapi.com"
        }
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        data = response.text
        try:
            d = pd.DataFrame(json.loads(data))
        except:
            continue
        d = d.iloc[[0]]
        d = d.rename(index={'concentration': i})
        mumbai = pd.concat([mumbai, d])
    return mumbai


def Show_Air_Chart_View(request):
    data = get_data('https://www.aqi.in/dashboard/india/maharashtra/mumbai/')
    pm2_graph = px.bar(data, x="LOCATIONS", y='PM2.5')
    pm2_graph = pm2_graph.to_html()
    pm10_graph = px.bar(data, x="LOCATIONS", y='PM10')
    pm10_graph = pm10_graph.to_html()
    aqi_in_graph = px.bar(data, x="LOCATIONS", y='AQI-IN')
    aqi_in_graph = aqi_in_graph.to_html()
    # file = open('/static/mumbai_dataset.csv')
    d = pd.read_csv("D:\\fun\\html\\air_pollution\\static\\mumbai_dataset.csv")
    air_graph = px.bar(d, x="location", y=[
                       'CO', 'NO2', 'O3', 'SO2', 'PM2.5', 'PM10'], title="Air Particle In Mumbai")
    air_graph = air_graph.to_html()
    context = {
        "pm2_graph": pm2_graph,
        "pm10_graph": pm10_graph,
        "aqi_in_graph": aqi_in_graph,
        "air_graph": air_graph,
    }
    return render(request, "index.html", context)
