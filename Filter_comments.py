import re
from Keywords import all_keywords

# Percorso del file di input e output
input_path = 'D:\\natural lenguages\\progetto\\output_comments.txt'
output_path = 'D:\\natural lenguages\\progetto\\filtered_comments.txt'

keywords = all_keywords

def is_relevant_comment(comment_text, keywords):
    # Verifica se una delle espressioni regolari è presente nel commento
    return any(re.search(keyword, comment_text, re.IGNORECASE) for keyword in keywords)

# Apertura del file di input e output
with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    current_game_data = {}  # Per memorizzare i dati del gioco corrente

    for line in infile:
        # Gestisci ogni riga con un controllo sulla presenza di dati
        if line.startswith("Game ID:"):
            parts = line.strip().split(": ", 1)
            if len(parts) > 1:
                current_game_data["game_id"] = parts[1]
        elif line.startswith("Game Name:"):
            parts = line.strip().split(": ", 1)
            if len(parts) > 1:
                current_game_data["game_name"] = parts[1]
        elif line.startswith("Comment ID:"):
            parts = line.strip().split(": ", 1)
            if len(parts) > 1:
                current_game_data["comment_id"] = parts[1]
        elif line.startswith("Comment Text:"):
            parts = line.strip().split(": ", 1)
            if len(parts) > 1:
                current_game_data["comment_text"] = parts[1]
        elif line.startswith("Rating:"):
            parts = line.strip().split(": ", 1)
            if len(parts) > 1:
                current_game_data["rating"] = parts[1]

                # Verifica se il commento è rilevante dopo aver raccolto tutti i dati
                comment_text = current_game_data.get("comment_text", "")
                if is_relevant_comment(comment_text, keywords):
                    # Scrivi il commento filtrato nel file di output
                    outfile.write(f"Game ID: {current_game_data['game_id']}\n")
                    outfile.write(f"Game Name: {current_game_data['game_name']}\n")
                    outfile.write(f"Comment ID: {current_game_data['comment_id']}\n")
                    outfile.write(f"Comment Text: {current_game_data['comment_text']}\n")
                    outfile.write(f"Rating: {current_game_data['rating']}\n")
                    outfile.write("-" * 50 + "\n")  # Separatore tra i commenti

print(f"Commenti filtrati salvati in {output_path}")

