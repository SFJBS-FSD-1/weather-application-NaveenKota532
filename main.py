###this is a flask app which queries data from openweathermap api
###http://api.openweathermap.org/data/2.5/weather?q=delhi&appkey=997ea79e1c9575bd4f087cf90e68205d
##here delhi is the city and appkey is the key given to us once we register with openweathermap org for api access
#you can create an account with them to get the api key, my key is 64cff2665ccc1450e021de170ba99e4b
#prashams key 997ea79e1c9575bd4f087cf90e68205d
#this program weather_app.py is the controller and weatherapp_homepage.html handles view part in the MVC architecture
#if you run the program before your email is verified by openweathermap you will get unauthorised error
#urllib.error.HTTPError: HTTP Error 401: Unauthorized
#my key is not working

from flask import Flask,render_template,request
import urllib.request
import json
import requests
import datetime
from pytz import timezone
import os

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def homepage():
    if request.method=="POST":
        city=request.form["city"]
        print(city)
        api_key = "997ea79e1c9575bd4f087cf90e68205d"
        url= "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid="+api_key+"&units=metric"
        print(url)
        api_data_from_url = requests.get(url).json()
        print(api_data_from_url)
        if api_data_from_url["cod"]=="404":
            data = {"message":api_data_from_url["message"],"status":404}
            return render_template("weatherapp_homepage.html", mydata=data)
        elif api_data_from_url["cod"]=="400":
            data = {"message":api_data_from_url["message"],"status":400}
            return render_template("weatherapp_homepage.html", mydata=data)
        elif api_data_from_url["cod"]== 200:
            data = {"city":api_data_from_url["name"],"latitude":api_data_from_url["coord"]["lat"],
                    "longitude":api_data_from_url["coord"]["lon"],
                    "temperature":round(api_data_from_url["main"]["temp"],2),
                    "sunrise":datetime.datetime.fromtimestamp(api_data_from_url["sys"]["sunrise"]),
                    "sunset":datetime.datetime.fromtimestamp(api_data_from_url["sys"]["sunset"],tz=timezone("Asia/Kolkata")),
                    "status":200}
            return render_template("weatherapp_homepage.html",mydata=data)
    else:
        data=None
        return render_template("weatherapp_homepage.html",mydata=data)
#we are sending data to html file using the parameter mydata
#we need to access this mydata in html file and print it
port = int(os.environ.get("PORT",5000))
if __name__ == "__main__":
    app.run(port=port)
