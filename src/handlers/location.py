from telegram import Update
from telegram.ext import ContextTypes

from db.queries import set_user_coordinates


async def location_handler(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    """
    Response for a location-sharing message. It stores it in the database.
    """
    assert (
        update.message is not None
        and update.message.location is not None
        and update.effective_user is not None
    )

    location = update.message.location

    await set_user_coordinates(
        update.effective_user.id,
        location.latitude,
        location.longitude,
    )

    _ = await update.message.reply_text(
        'Tu ubicación a sido actualizada. La recordaré para futuras peticiones.'
    )


async def please_update_location_handler(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
):
    """
    Response to ask the user to update their location.
    """
    assert update.message is not None

    # I'm aware that I could create a button that asks for the user's location
    # via a dialog. However, I believe once the user learns that they can share
    # it this way, directly sharing is better DX.
    _ = await update.message.reply_text(
        'Por favor, comparte una ubicación con nosotros. Mediante la interfaz de telegram, como en cualquier otro chat.'
    )
