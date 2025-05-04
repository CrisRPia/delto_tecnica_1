from typing import NamedTuple

from db.helpers import get_connection


async def insert_user(user_id: int):
    async with get_connection() as connection:
        _ = await connection.execute(
            """
            INSERT
              INTO users(telegram_id)
            VALUES :user_id;
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
              INTO users(telegram_id)
            VALUES (:telegram_id)
                    ON CONFLICT (telegram_id) DO UPDATE SET counter = counter + 1
         RETURNING counter;
        """,
            {'user_id': user_id, 'counter': 1},
        )

        row = await result.fetchone()

        assert row is not None and isinstance(row[0], int)

        await connection.commit()
        return row[0]  # pyright: ignore [reportAny]


async def set_user_coordinates(user_id: int, latitude: float, longitude: float):
    async with get_connection() as connection:
        _ = await connection.execute(
            """
                INSERT
                  INTO users(telegram_id, latitude, longitude)
                VALUES (:user_id, :latitude, :longitude)
                    ON CONFLICT (telegram_id) DO UPDATE SET latitude = :latitude, longitude = :longitude
            """,
            {
                'user_id': user_id,
                'latitude': latitude,
                'longitude': longitude,
            },
        )

        await connection.commit()


class UserRow(NamedTuple):
    telegram_id: int
    counter: int
    latitude: float | None = None
    longitude: float | None = None


async def get_user(user_id: int) -> UserRow | None:
    async with get_connection() as connection:
        result = await connection.execute(
            """
            SELECT telegram_id, counter, latitude, longitude
              FROM users
             WHERE telegram_id = :user_id;
        """,
            {'user_id': user_id},
        )

        row = await result.fetchone()

        if row is None:
            return None

        return UserRow._make(row)
