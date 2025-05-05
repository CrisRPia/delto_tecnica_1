import os
from typing import Literal, NotRequired, TypedDict, final
import aiohttp
from .openweather_get_response_codegen import WeatherData

OPENWEATHER_KEY_PATH = 'OPENWEATHER_API_KEY'
OPENWEATHER_TOKEN = os.environ[OPENWEATHER_KEY_PATH]


class GetWeatherParams(TypedDict):
    lat: float
    lon: float
    units: NotRequired[Literal['standard', 'metric', 'imperial']]
    exclude: NotRequired[
        Literal[
            'current',
            'minutely',
            'hourly',
            'daily',
            'alerts',
        ]
    ]
    lang: NotRequired[str]


@final
class OpenWeatherClient:
    """
    Helper class that shares an OpenWeather token across multiple requests.
    """

    baseUrl = 'https://api.openweathermap.org/data/2.5/weather'

    def __init__(self, token: str | None = None) -> None:
        if token is None:
            self.token = OPENWEATHER_TOKEN
            return

        self.token = token

    async def get_weather(self, opts: GetWeatherParams) -> WeatherData:
        async with aiohttp.ClientSession() as session:
            url = self.baseUrl
            params: list[str] = [f'appid={self.token}']

            params += [f'{option}={value}' for option, value in opts.items()]

            async with session.get(
                url=url, params='&'.join(params)
            ) as response:
                text = await response.text()
                try:
                    return WeatherData.model_validate_json(text)
                except:
                    raise Exception("Error while parsing: " + text)
