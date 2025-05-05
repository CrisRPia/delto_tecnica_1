CREATE TABLE users (
    telegram_id INT PRIMARY KEY,
    counter     INT NOT NULL DEFAULT 1,
    latitude    FLOAT        DEFAULT NULL,
    longitude   FLOAT        DEFAULT NULL
);

CREATE TABLE fun_facts (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id             INTEGER NOT NULL,
    fun_fact_summary    TEXT    NOT NULL,
    timestamp           DATETIME DEFAULT CURRENT_TIMESTAMP,
    counter_at_creation INT     NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (telegram_id)
);
