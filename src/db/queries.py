"""
Collection of all queries made in the app.

Many of them try to insert a new user first, and then update the actual data
they want to update. I did it this way because I believe it is possible to run
the commands in any order, which means /start needn't be first, and so I chose
for most queries to work fine if used by a new user. -- CR
"""

from typing import NamedTuple

from db.helpers import get_connection


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
            VALUES (:user_id)
                    ON CONFLICT (telegram_id) DO UPDATE SET counter = counter + 1
         RETURNING counter;
        """,
            {'user_id': user_id, 'counter': 1},
        )

        row = await result.fetchone()

        assert row is not None and isinstance(row[0], int)

        # I lost way more time than I should have forgetting to commit db
        # changes -- CR
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


class FunFactRow(NamedTuple):
    fun_fact_summary: int
    counter_at_creation: int
    timestamp: str


async def get_users_fun_facts(user_id: int) -> list[FunFactRow]:
    async with get_connection() as connection:
        result = await connection.execute(
            """
            SELECT fun_fact_summary, counter_at_creation, timestamp
              FROM fun_facts where user_id = :user_id
             ORDER BY timestamp DESC
             LIMIT 20;
        """,
            {'user_id': user_id},
        )

        rows = await result.fetchall()

        return [FunFactRow._make(row) for row in rows]


async def insert_fun_fact(user_id: int, fun_fact_summary: str):
    """
    Inserts a new fun fact summary in the database. This will error if `user_id`
    does not already exist within the database. This is intentional, because
    /ai is not an entry point by design.
    """
    async with get_connection() as connection:
        _ = await connection.execute(
            """
                INSERT
                  INTO fun_facts (user_id, fun_fact_summary, counter_at_creation)
                VALUES (:user_id, :fun_fact_summary, (
                    SELECT counter
                      FROM users
                     WHERE users.telegram_id = :user_id
                ));
            """,
            {'user_id': user_id, 'fun_fact_summary': fun_fact_summary},
        )

        await connection.commit()
