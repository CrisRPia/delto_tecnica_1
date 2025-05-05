from telegram import Update
from telegram.ext import ContextTypes


async def start_handler(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    A greeting response.
    """
    assert update.message is not None

    _ = await update.message.reply_text(
        '¡Hola! Soy el bot de Telegram de Cristian Rodríguez. ¿Quieres contar o saber del clima en to zona?\n'
        + 'Tienes disponible un menú para ver todos mis posibles comandos.'
    )
