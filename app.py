from flask import Flask, render_template, request
from weather import get_weather
from traduction import weather_dict
from country import country_dict


# Création de l'application Flask
app = Flask(__name__, template_folder='templates')

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Traitement du formulaire de recherche
@app.route('/', methods=['POST'])
def get_weather_data():
    city = request.form['city']
    weather_data = get_weather(city)
    if weather_data is None:
        message = "Désolé, nous n'avons pas pu récupérer les données météorologiques pour cette ville."
        return render_template('index.html', message=message)
    
    else:
        description = weather_data['weather'][0]['description']
        if description in weather_dict:
            description_fr = weather_dict[description]

        country = weather_data['sys']['country']
        if country in country_dict:
            country = country_dict[country]

        data = {
            'city': city,
            'country': country,
            'description': description_fr,
            'temp': round(weather_data['main']['temp'] - 273.15, 2),
            'temp_min': round(weather_data['main']['temp_min'] - 273.15, 2),
            'temp_max': round(weather_data['main']['temp_max'] - 273.15, 2),
            'pressure': weather_data['main']['pressure'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'wind_deg': weather_data['wind']['deg'],
            'visibility': weather_data['visibility'],
            'latitude': weather_data['coord']['lat'],
            'longitude': weather_data['coord']['lon']
        }
        return render_template('weather.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)