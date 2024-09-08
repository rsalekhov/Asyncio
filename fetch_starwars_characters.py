import aiohttp
import asyncio
import aiosqlite
from urllib.parse import urlparse

# Базовый URL API
BASE_URL = 'https://swapi.dev/api/people/'

# Функция для получения названия по URL (фильмы, корабли, виды и т.д.)
async def fetch_name_from_url(session, url):
    async with session.get(url) as response:
        data = await response.json()
        return data.get('title') or data.get('name')

# Функция для получения информации о персонаже
async def fetch_character(session, character_id):
    async with session.get(f'{BASE_URL}{character_id}/') as response:
        if response.status == 404:
            return None
        return await response.json()

# Обработка данных персонажа
async def process_character(session, character_data):
    films = await asyncio.gather(*[fetch_name_from_url(session, film_url) for film_url in character_data['films']])
    species = await asyncio.gather(*[fetch_name_from_url(session, species_url) for species_url in character_data['species']])
    starships = await asyncio.gather(*[fetch_name_from_url(session, starship_url) for starship_url in character_data['starships']])
    vehicles = await asyncio.gather(*[fetch_name_from_url(session, vehicle_url) for vehicle_url in character_data['vehicles']])
    homeworld = await fetch_name_from_url(session, character_data['homeworld'])

    return {
        'id': int(urlparse(character_data['url']).path.split('/')[-2]),
        'name': character_data['name'],
        'birth_year': character_data['birth_year'],
        'eye_color': character_data['eye_color'],
        'gender': character_data['gender'],
        'hair_color': character_data['hair_color'],
        'height': character_data['height'],
        'mass': character_data['mass'],
        'skin_color': character_data['skin_color'],
        'homeworld': homeworld,
        'films': ', '.join(films),
        'species': ', '.join(species),
        'starships': ', '.join(starships),
        'vehicles': ', '.join(vehicles),
    }

# Вставка данных в базу
async def insert_character(db, character):
    query = '''
    INSERT OR REPLACE INTO characters (id, name, birth_year, eye_color, gender, hair_color, height, mass, skin_color, homeworld, films, species, starships, vehicles)
    VALUES (:id, :name, :birth_year, :eye_color, :gender, :hair_color, :height, :mass, :skin_color, :homeworld, :films, :species, :starships, :vehicles)
    '''
    await db.execute(query, character)
    await db.commit()

# Основная функция для получения всех персонажей и записи их в базу данных
async def fetch_and_store_characters():
    async with aiohttp.ClientSession() as session, aiosqlite.connect('starwars.db') as db:
        character_id = 1
        while True:
            character_data = await fetch_character(session, character_id)
            if character_data is None:
                break  # Прекратить выполнение, если больше нет персонажей

            processed_character = await process_character(session, character_data)
            await insert_character(db, processed_character)

            print(f"Загружен персонаж: {processed_character['name']}")
            character_id += 1

# Запуск основной функции
if __name__ == "__main__":
    asyncio.run(fetch_and_store_characters())
