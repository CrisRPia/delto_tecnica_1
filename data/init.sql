CREATE TABLE users (
    telegram_id INT PRIMARY KEY,
    counter     INT NOT NULL DEFAULT 1,
    latitude    FLOAT        DEFAULT NULL,
    longitude   FLOAT        DEFAULT NULL
);

INSERT
  INTO users(telegram_id, counter, latitude, longitude)
VALUES (:telegram_id, :counter, DEFAULT, DEFAULT)
    ON CONFLICT (telegram_id) DO UPDATE SET latitude = :latitude
     , longitude                       = :longitude;

select * from users;