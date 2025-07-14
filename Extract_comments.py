import pandas as pd
import requests
import xml.etree.ElementTree as ET
import time


file_path = 'D:\\natural lenguages\\boardgames_ranks.csv' 
df = pd.read_csv(file_path)

games = list(zip(df['id'], df['name']))


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

#Crea un file di output per scrivere i dati
output_path = 'D:\\natural lenguages\\Progetto\\output_comments.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    # Itera su ciascun gioco e recupera i commenti
    for game_id, name in games:
        comments = get_game_comments(game_id)
        print(f"commenti del gioco {game_id, name}")
        for comment in comments:
            # Scrivi ogni commento con i dettagli nel file
            f.write(f"Game ID: {game_id}\n")
            f.write(f"Game Name: {name}\n")
            f.write(f"Comment ID: {comment['comment_id']}\n")
            f.write(f"Comment Text: {comment['text']}\n")
            f.write(f"Rating: {comment['rating']}\n")
            f.write("-" * 50 + "\n")  # Separatore tra i commenti
        f.write("=" * 50 + "\n")  # Separatore tra i giochi

'''
output_path = 'D:\\natural lenguages\\output_comments.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    # Recupera e scrivi i commenti solo per il gioco con ID 224517
    comments = get_game_comments(game_id)
    for comment in comments:
        # Scrivi ogni commento con i dettagli nel file
        f.write(f"Game ID: {game_id}\n")
        f.write(f"Game Name: {game_name}\n")
        f.write(f"Comment ID: {comment['comment_id']}\n")
        f.write(f"Comment Text: {comment['text']}\n")
        f.write(f"Rating: {comment['rating']}\n")
        f.write("-" * 50 + "\n")  # Separatore tra i commenti
'''


print(f"Commenti salvati in {output_path}")
