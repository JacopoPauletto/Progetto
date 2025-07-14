import re
import spacy

# Carica il modello linguistico di spaCy per l'inglese
nlp = spacy.load("en_core_web_sm")

# Percorso del file di input e del file di output
input_path = 'D:\\natural lenguages\\progetto\\filtered_comments.txt'
output_path = 'D:\\natural lenguages\\progetto\\cleaned_comments.txt'

def preprocess_comment(text):

    # Converte il testo in minuscolo
    text = text.lower()
    
    # Rimuove URL e caratteri speciali (es. BBCode)
    text = re.sub(r"http\S+|www\S+|https\S+|[\[\]()*&%$#@!_+={}|<>]", "", text)
    
    # Processa il testo con spaCy per rimuovere stopwords, lemmatizzare e mantenere solo parole alfabetiche
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    
    # Ricrea il testo pre-processato a partire dai token
    return " ".join(tokens)

# Elabora il file riga per riga
with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    current_comment = {}  # Dizionario per salvare i dati del commento corrente
    
    for line in infile:
        # Controlla e processa i dati del commento
        if line.startswith("Game ID:"):
            current_comment["game_id"] = line.strip().split(": ", 1)[1]
        elif line.startswith("Game Name:"):
            current_comment["game_name"] = line.strip().split(": ", 1)[1]
        elif line.startswith("Comment ID:"):
            current_comment["comment_id"] = line.strip().split(": ", 1)[1]
        elif line.startswith("Comment Text:"):
            raw_text = line.strip().split(": ", 1)[1]
            # Applica il preprocessing al testo del commento
            current_comment["cleaned_text"] = preprocess_comment(raw_text)
        elif line.startswith("Rating:"):
            current_comment["rating"] = line.strip().split(": ", 1)[1]
            
            # Una volta che il commento è completo, scrivilo nel file di output
            outfile.write(f"Game ID: {current_comment['game_id']}\n")
            outfile.write(f"Game Name: {current_comment['game_name']}\n")
            outfile.write(f"Comment ID: {current_comment['comment_id']}\n")
            outfile.write(f"Cleaned Comment Text: {current_comment['cleaned_text']}\n")
            outfile.write(f"Rating: {current_comment['rating']}\n")
            outfile.write("-" * 50 + "\n")  # Separatore tra i commenti

print(f"Commenti puliti e preprocessati salvati in {output_path}")
