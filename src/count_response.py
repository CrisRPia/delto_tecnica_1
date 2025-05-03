from telegram import Update
from telegram.ext import ContextTypes

# Placeholder, will use db
counter = 0


async def increase_user_count(_userId: int) -> int:
    global counter
    counter += 1
    return counter


async def count_response(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        raise NotImplementedError()

    if update.effective_user is None:
        _ = update.message.reply_text('Lo siento, no te pudimos identificar.')
        return

    new_count = await increase_user_count(_userId=update.effective_user.id)

    _ = await update.message.reply_text(
        f'¡Después del {new_count - 1} va el {new_count}! \n'
        + f'Míralo en sandías: {'🍉' * min((999, new_count))}'
    )
