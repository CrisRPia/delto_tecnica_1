from typing import NamedTuple
from db.helpers import get_connection


async def insert_user(user_id: int):
    async with get_connection() as connection:
        _ = await connection.execute(
            """
            INSERT
              INTO users(telegram_id, counter)
            VALUES (:user_id, 0);
        """,
            {'user_id': user_id},
        )


async def increase_user_count(user_id: int) -> int:
    """
    Returns new count value.
    If the user does not exist, it creates a new user with a count of 1.
    """
    async with get_connection() as connection:
        result = await connection.execute(
            """
               INSERT
                 INTO users (telegram_id, counter)
               VALUES (:user_id, 1)
                   ON CONFLICT DO UPDATE SET counter = counter + 1
            RETURNING counter;
        """,
            {'user_id': user_id},
        )

        row = await result.fetchone()

        assert row is not None and isinstance(row[0], int)

        await connection.commit()
        return row[0]  # pyright: ignore [reportAny]


class UserRow(NamedTuple):
    telegram_id: int
    counter: int


async def get_user(user_id: int) -> UserRow | None:
    async with get_connection() as connection:
        result = await connection.execute(
            """
            SELECT telegram_id, counter
              FROM users
             WHERE telegram_id = $1;
        """,
            [user_id],
        )

        row = await result.fetchone()

        if row is None:
            return None

        return UserRow._make(row)
