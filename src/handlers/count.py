from telegram import Update
from telegram.ext import ContextTypes

from db.queries import increase_user_count


async def count_handler(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    Increases the user's counter and sends them a message with it.
    """
    assert update.message and update.effective_user

    new_count = await increase_user_count(user_id=update.effective_user.id)

    _ = await update.message.reply_text(
        f'¡Después del {new_count - 1} va el {new_count}! \n'
        + f'Míralo en sandías: {'🍉' * min((999, new_count))}'
    )
