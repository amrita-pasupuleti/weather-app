from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    if not city or not city.strip():
        # If the city input is empty or contains only spaces, return the form with an error message
        return render_template('index.html', error="Please enter a city name.")

    weather_data = get_current_weather(city)

    # City is not found by API
    if weather_data['cod'] != 200:
        return render_template('index.html', error="City not found. Please try again.")

    return render_template(
        "index.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
