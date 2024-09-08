CREATE TABLE IF NOT EXISTS characters (
    id INTEGER PRIMARY KEY,       -- ID персонажа
    name TEXT NOT NULL,           -- Имя персонажа
    birth_year TEXT,              -- Год рождения
    eye_color TEXT,               -- Цвет глаз
    gender TEXT,                  -- Пол
    hair_color TEXT,              -- Цвет волос
    height TEXT,                  -- Рост
    mass TEXT,                    -- Вес
    skin_color TEXT,              -- Цвет кожи
    homeworld TEXT,               -- Родная планета
    films TEXT,                   -- Фильмы через запятую
    species TEXT,                 -- Виды через запятую
    starships TEXT,               -- Корабли через запятую
    vehicles TEXT                 -- Транспорт через запятую
);
