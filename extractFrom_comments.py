import pandas as pd
import requests
import xml.etree.ElementTree as ET
import time

# Percorso del file CSV
file_path = 'D:\\natural lenguages\\boardgames_ranks.csv'
df = pd.read_csv(file_path)

# Filtra i giochi a partire dalla riga 95329
filtered_games = df.iloc[95328:]  # Ricorda: il DataFrame è 0-indexed, quindi 95329 corrisponde all'indice 95328

# Crea una lista di tuple (game_id, game_name)
games = list(zip(filtered_games['id'], filtered_games['name']))

def get_game_comments(game_id, max_pages=5):
    comments = []
    for page in range(1, max_pages + 1):
        url = f'https://boardgamegeek.com/xmlapi2/thing?id={game_id}&comments=1&page={page}'
        response = requests.get(url)
        if response.status_code != 200:
            break

        root = ET.fromstring(response.content)
        for comment in root.findall(".//comment"):
            comments.append({
                "comment_id": comment.get("id"),
                "text": comment.get("value"),
                "rating": comment.get("rating")
            })
        #time.sleep(1)
    return comments

# Percorso del file di output
output_path = 'D:\\natural lenguages\\Progetto\\output_comments_from_row_95329.txt'

# Scrivi i commenti nel file di output
with open(output_path, 'w', encoding='utf-8') as f:
    for game_id, name in games:
        print(f"Estrazione commenti per il gioco ID {game_id}: {name}")
        comments = get_game_comments(game_id)
        for comment in comments:
            f.write(f"Game ID: {game_id}\n")
            f.write(f"Game Name: {name}\n")
            f.write(f"Comment ID: {comment['comment_id']}\n")
            f.write(f"Comment Text: {comment['text']}\n")
            f.write(f"Rating: {comment['rating']}\n")
            f.write("-" * 50 + "\n")  # Separatore tra i commenti
        f.write("=" * 50 + "\n")  # Separatore tra i giochi

print(f"Commenti salvati in {output_path}")
