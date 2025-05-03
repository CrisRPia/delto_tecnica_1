import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_KEY_PATH = 'TELEGRAM_API_KEY'


async def default_response(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        raise NotImplementedError('TODO: Understand why this could happen.')

    _ = await update.message.reply_text(
        '¡Hola! Soy el bot de Telegram de Cristian Rodríguez. ¿Quieres contar o saber del clima en to zona?'
    )


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
