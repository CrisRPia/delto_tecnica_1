from telegram import Update
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from apis.openweather import OpenWeatherClient
from db.queries import get_user
from location_response import please_update_location_response

WEATHER_CLIENT = OpenWeatherClient()


async def weather_request_response(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    assert update.effective_user is not None and update.message is not None
    user = await get_user(update.effective_user.id)

    if user is None or user.longitude is None or user.latitude is None:
        return await please_update_location_response(update, context)

    weather = await WEATHER_CLIENT.get_weather(
        {
            'lat': user.latitude,
            'lon': user.longitude,
            'lang': 'es',
            'units': 'metric',
        }
    )

    # Shortened this just so that the `response` string is more readable.
    def mdv2(text: str):
        return escape_markdown(text, version=2)

    def mdv2round(number: float):
        return mdv2(f'{number:.1f}')

    response = f"""
🌍 El clima en *{mdv2(weather.name)}, {mdv2(weather.sys.country)}*: *{mdv2(weather.weather[0].description)}*\\.

🌡️ *Temperatura:*
  Actual: {mdv2round(weather.main.temp)}°C
  Sensación térmica: {mdv2round(weather.main.feels_like)}°C
  Mínima: {mdv2round(weather.main.temp_min)}°C
  Máxima: {mdv2round(weather.main.temp_max)}°C

💧 *Humedad:* {weather.main.humidity}%

💨 *Viento:* {mdv2round(weather.wind.speed)} m/s

☁️ *Nubosidad:* {weather.clouds.all}%
"""

    _ = await update.message.reply_text(
        response, parse_mode=ParseMode.MARKDOWN_V2
    )
