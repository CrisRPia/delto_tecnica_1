import os
from telegram.ext import ApplicationBuilder, CommandHandler
from apis.openweather import OpenWeatherClient
import count_response
from db.helpers import reinit_if_no_db
import default_response

TELEGRAM_KEY_PATH = 'TELEGRAM_API_KEY'
TELEGRAM_TOKEN = os.environ[TELEGRAM_KEY_PATH]

COMMANDS = [
    CommandHandler('start', default_response.default_response),
    CommandHandler('count', count_response.count_response),
]


async def on_bot_start(_):
    print('Bot iniciado.')
    await reinit_if_no_db()
    print('Base de datos funcional.')


def dev():
    app = (
        ApplicationBuilder()
        .token(TELEGRAM_TOKEN)
        .post_init(on_bot_start)
        .build()
    )
    for command in COMMANDS:
        app.add_handler(command)

    print('Iniciando bot...')
    app.run_polling()


if __name__ == '__main__':
    dev()
