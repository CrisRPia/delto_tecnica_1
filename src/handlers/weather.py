from telegram import Update
from telegram.helpers import escape_markdown
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from apis.openweather import DEFAULT_WEATHER_CLIENT
from db.queries import get_user
from handlers.location import please_update_location_response


async def weather_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Verifies if user has shared a location and, if so, sends them a summary
    of their weather. It uses a precise location shared by the user instead
    of a city name.

    I am aware openweather can accept a city name, but I think this method
    offers more flexibility, precision, and DX. -- CR
    """
    assert update.effective_user and update.message

    user = await get_user(update.effective_user.id)
    if not user or not user.longitude is not None or user.latitude is None:
        return await please_update_location_response(update, context)

    weather = await DEFAULT_WEATHER_CLIENT.get_weather(
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

    # I need to do this check because there will be no country information if
    # the location is, say, the Pacitic Ocean.
    country = weather.sys.country
    country_string = (
        mdv2(', ' + country)
        if country
        else f'{mdv2round(user.latitude)}, {mdv2round(user.longitude)}'
    )

    response = f"""
🌍 El clima en *{mdv2(weather.name)}{country_string}*: *{mdv2(weather.weather[0].description)}*\\.

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
