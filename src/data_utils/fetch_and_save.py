import os
import time
from dotenv import load_dotenv
import requests
import pandas as pd

load_dotenv()
API_KEY = os.getenv('RAWG_API_KEY')
BASE_URL = 'https://api.rawg.io/api'

def get_details(game_id: int):
    url = f'{BASE_URL}/games/{game_id}'
    params = {'key': API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def save_chunk(chunk: list, filename: str, first_chunk: bool):
    df = pd.DataFrame(chunk)
    df.to_csv(filename, mode='w' if first_chunk else 'a', header=first_chunk, index=False)
    print(f'Saved chunk of {len(chunk)} games to {filename}')

def get_games(num_games: int, output_filename: str, delay=1.0, chunk_size=1000, start_index=0):
    all_games = []
    default_page_size = 40
    num_pages = (num_games + default_page_size - 1) // default_page_size
    total_collected = start_index
    first_chunk = True

    start_page = (start_index // default_page_size) + 1
    for page in range(start_page, num_pages+1):
        remaining = num_games - total_collected
        page_size = min(default_page_size, remaining)
        print(f'Fetching list page {page} with page_size={page_size}...')
        
        url = f'{BASE_URL}/games'
        params = {
            'key': API_KEY,
            'page_size': page_size,
            'page': page,
            'ordering': '-added'
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f'Error {response.status_code} on page {page}')
            break

        games = response.json().get('results', [])
        for game in games:
            print(f'Fetching details for: {game["name"]} (ID: {game["id"]})')
            details = get_details(game['id'])
            if details:
                all_games.append({
                    'id': details.get('id'),
                    'name': details.get('name'),
                    'released': details.get('released'),
                    'rating': details.get('rating'),
                    'playtime': details.get('playtime'),
                    'ratings_count': details.get('ratings_count'),
                    'added': details.get('added'),
                    'genres': [g['name'] for g in details.get('genres')],
                    'tags': [t['name'] for t in details.get('tags', [])],
                    'description_raw': details.get('description_raw', '')
                })
                total_collected += 1
                time.sleep(delay)

                if len(all_games) >= chunk_size:
                    save_chunk(all_games, output_filename, first_chunk)
                    first_chunk = False
                    all_games = []
        
            if total_collected >= num_games:
                break
        
        if total_collected >= num_games:
            break
    
    if all_games:
        save_chunk(all_games, output_filename, first_chunk)
    
    print(f'Finished. Total games collected: {total_collected}')

# get_games(num_games=_, output_filename=_)