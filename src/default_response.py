from telegram import Update
from telegram.ext import ContextTypes

async def default_response(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        raise NotImplementedError('TODO: Understand why this could happen.')

    _ = await update.message.reply_text(
        '¡Hola! Soy el bot de Telegram de Cristian Rodríguez. ¿Quieres contar o saber del clima en to zona?'
    )

    # TODO: Give command-run instructions or buttons.

