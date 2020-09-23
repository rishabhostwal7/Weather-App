import requests
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

def ep_to_day(ep):
    return datetime.fromtimestamp(ep).strftime("%A")

def ep_to_date(ep):
    return datetime.fromtimestamp(ep).strftime("%d %B")

def f_to_c(Fahrenheit):
    f = int(Fahrenheit) - 273.15
    res =  ('%.2f'%f)
    return res


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'



#db = SQLAlchemy(app)

#class City(db.Model):
#    id = db.column(db.Integer, primary_key=True)
#    name = db.column(db.String(50), null=False)

#db.create_all()
city = "Durg"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        global city
        
        city = request.form.get("city")
        return redirect(request.url)


    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&appid=afd31f25abd0625b4a26d7cf6a59cda8'
    try:
        r = requests.get(url.format(city)).json()
    except Exception as e:
        print("Please enter Right city")
        return render_template("error.html")

    inc = 0
    value=[inc,]                                         # increment value to get next day
    flag=True
    ep1 = r['list'][inc]['dt']
    formatted_day1 = ep_to_day(ep1)                 # Day 1 Data
    formatted_date1 = ep_to_date(ep1)
    inc+=1



    while(flag):                                    # Day 2 Data
        ep2 = r['list'][inc]['dt']
        formatted_day2 = ep_to_day(ep2)
        formatted_date2 = ep_to_date(ep2)
        if formatted_day2 == formatted_day1 or formatted_date1 == formatted_date2:
            inc+=1
            continue
        else:
            value.append(inc)
            inc+=1
            break


    while(flag):                                    # Day 3 Data
        ep3 = r['list'][inc]['dt']
        formatted_day3 = ep_to_day(ep3)
        formatted_date3 = ep_to_date(ep3)
        if formatted_day2 == formatted_day3 or formatted_date2 == formatted_date3:
            inc+=1
            continue
        else:
            value.append(inc)
            inc+=1
            break


    while(flag):                                    # Day 4 Data
        ep4 = r['list'][inc]['dt']
        formatted_day4 = ep_to_day(ep4)
        formatted_date4 = ep_to_date(ep4)
        if formatted_day3 == formatted_day4 or formatted_date3 == formatted_date4:
            inc+=1
            continue
        else:
            value.append(inc)
            inc+=1
            break

    while(flag):                                    # Day 5 Data
        ep5 = r['list'][inc]['dt']
        formatted_day5 = ep_to_day(ep5)
        formatted_date5 = ep_to_date(ep5)
        if formatted_day4 == formatted_day5 or formatted_date4 == formatted_date5:
            inc+=1
            continue
        else:
            value.append(inc)
            inc+=1
            break

# It's actually Kelvin not Fahrenheit

    Fahrenheit1 = int(r['list'][value[0]]['main']['temp'])
    Fahrenheit2 = int(r['list'][value[1]]['main']['temp'])
    Fahrenheit3 = int(r['list'][value[2]]['main']['temp'])
    Fahrenheit4 = int(r['list'][value[3]]['main']['temp'])
    Fahrenheit5 = int(r['list'][value[4]]['main']['temp'])

    Celsius1 = str(f_to_c(Fahrenheit1))
    Celsius2 = str(f_to_c(Fahrenheit2))
    Celsius3 = str(f_to_c(Fahrenheit3))
    Celsius4 = str(f_to_c(Fahrenheit4))
    Celsius5 = str(f_to_c(Fahrenheit5))


    def toTextualDescription(degree):
        if (degree>337.5):
            return 'Northerly'
        elif (degree>292.5):
            return 'North Westerly'
        elif (degree>247.5):
            return 'South Westerly'
        elif (degree>202.5):
            return 'Southerly'
        elif (degree>157.5):
            return 'North Westerly'
        elif (degree>122.5):
            return 'South Easterly'
        elif (degree>67.5):
            return 'Easterly'
        elif (degree>22.5):
            return 'North Easterly'
        else:
            return 'Northerly'


    weather0_degree = r['list'][value[0]]['wind']['deg']
    weather0_direction = toTextualDescription(weather0_degree)


    weather0 = {
        'city': city,
        'temperature': Celsius1,
        'humidity': r['list'][value[0]]['main']['humidity'],
        'speed': r['list'][value[0]]['wind']['speed'],
        'direction': weather0_direction,
        'description': r['list'][value[0]]['weather'][0]['description'],
        'icon': r['list'][value[0]]['weather'][0]['icon'],
        'day': formatted_day1,
        'date': formatted_date1
    }

    weather1 = {
        'temperature': Celsius2,
        'humidity': r['list'][value[1]]['main']['humidity'],
        'description': r['list'][value[1]]['weather'][0]['description'],
        'icon': r['list'][value[1]]['weather'][0]['icon'],
        'day': formatted_day2,
        'date': formatted_date2
    }

    weather2 = {
        'temperature': Celsius3,
        'humidity': r['list'][value[2]]['main']['humidity'],
        'description': r['list'][value[2]]['weather'][0]['description'],
        'icon': r['list'][value[2]]['weather'][0]['icon'],
        'day': formatted_day3,
        'date': formatted_date3
    }

    weather3 = {
        'temperature': Celsius4,
        'humidity': r['list'][value[3]]['main']['humidity'],
        'description': r['list'][value[3]]['weather'][0]['description'],
        'icon': r['list'][value[3]]['weather'][0]['icon'],
        'day': formatted_day4,
        'date': formatted_date4
    }

    weather4 = {
        'temperature': Celsius5,
        'humidity': r['list'][value[4]]['main']['humidity'],
        'description': r['list'][value[4]]['weather'][0]['description'],
        'icon': r['list'][value[4]]['weather'][0]['icon'],
        'day': formatted_day5,
        'date': formatted_date5
    }

    print(weather0)
    print(weather1)
    print(weather2)
    print(weather3)
    print(weather4)
    print(r)

    return render_template('index.html', weather = [weather0,weather1, weather2, weather3, weather4])


#    return render_template('index.html', weather = weather)

app.run(port=5000, debug=True)
