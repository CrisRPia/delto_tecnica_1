import os
import sys
from telegram.ext import ApplicationBuilder, CommandHandler

from default_response import default_response

TELEGRAM_KEY_PATH = 'TELEGRAM_API_KEY'


def dev():
    print('Iniciando bot...')

    token = os.getenv(TELEGRAM_KEY_PATH)

    if token is None:
        print(
            f'Debes incluir el token de tu chat de telegram en {TELEGRAM_KEY_PATH}'
        )
        return sys.exit(1)

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler('start', default_response))
    app.run_polling()


if __name__ == '__main__':
    dev()
