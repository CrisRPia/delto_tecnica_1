import os
from pathlib import Path
import aiosqlite


PARENT_DIR = Path(__file__).resolve().parent
DATA_DIR = PARENT_DIR.parent.parent / 'data'
DB_PATH = DATA_DIR / 'data.db'
INIT_PATH = DATA_DIR / 'init.sql'


def get_connection() -> aiosqlite.Connection:
    return aiosqlite.connect(DB_PATH)


async def reinit_if_no_db():
    if os.path.isfile(DB_PATH):
        return

    with open(INIT_PATH) as init_file:
        init = init_file.read()

    async with get_connection() as conn:
        _ = await conn.executescript(init)
