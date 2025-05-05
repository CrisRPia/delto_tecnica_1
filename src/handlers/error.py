from telegram import Update
from telegram.ext import ContextTypes


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends an error message to the user when their request fails.
    """

    if isinstance(update, Update) and update.effective_chat and update.message:
        _ = await update.message.reply_text(
            'Hubo un error al procesar tu solicitud.'
        )

    assert context.error
    raise context.error
