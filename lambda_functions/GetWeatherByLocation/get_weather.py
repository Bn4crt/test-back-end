import json
import requests
import os

def _response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
        },
        "body": json.dumps(body_dict)
    }

def lambda_handler(event, context):
    try:
        params = event.get("queryStringParameters", {}) or {}
        location = params.get("location")
        lat = params.get("lat")
        lon = params.get("lon")

        if not location and not (lat and lon):
            return _response(400, {"error": "No location or coordinates provided"})

        api_key = os.environ.get("WEATHER_API_KEY")
        if not api_key:
            return _response(500, {"error": "Missing WEATHER_API_KEY in environment"})

        if lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

        response = requests.get(url, timeout=3)
        response.raise_for_status()

        data = response.json()
        temperature = data.get("main", {}).get("temp")
        condition = data.get("weather", [{}])[0].get("main")
        city = data.get("name")

        if temperature is None or condition is None or city is None:
            return _response(500, {"error": "Incomplete weather data received"})

        return _response(200, {
            "location": city,
            "temperature": temperature,
            "condition": condition
        })

    except requests.exceptions.Timeout:
        return _response(504, {"error": "Request to OpenWeatherMap timed out"})
    except requests.exceptions.RequestException as e:
        return _response(502, {"error": f"Weather service error: {str(e)}"})
    except Exception as e:
        return _response(500, {"error": f"Internal server error: {str(e)}"})
