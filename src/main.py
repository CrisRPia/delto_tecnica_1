import os
import sys
from telegram.ext import ApplicationBuilder, CommandHandler

import count_response
from db.helpers import reinit_if_no_db
import default_response

TELEGRAM_KEY_PATH = 'TELEGRAM_API_KEY'

COMMANDS = [
    CommandHandler('start', default_response.default_response),
    CommandHandler('count', count_response.count_response),
]


async def on_bot_start(_):
    print("Bot iniciado.")
    await reinit_if_no_db()
    print("Base de datos funcional.")

def dev():
    token = os.getenv(TELEGRAM_KEY_PATH)

    if token is None:
        print(
            f'Debes incluir el token de tu chat de telegram en {TELEGRAM_KEY_PATH}'
        )
        return sys.exit(1)

    app = ApplicationBuilder().token(token).post_init(on_bot_start).build()
    for command in COMMANDS:
        app.add_handler(command)

    print('Iniciando bot...')
    app.run_polling()


if __name__ == '__main__':
    dev()
