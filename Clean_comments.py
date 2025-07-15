import re
import spacy

nlp = spacy.load("en_core_web_sm")

input_path = 'D:\\natural lenguages\\progetto\\filtered_comments.txt'
output_path = 'D:\\natural lenguages\\progetto\\cleaned_comments.txt'

def preprocess_comment(text):

    text = text.lower()
    
    text = re.sub(r"http\S+|www\S+|https\S+|[\[\]()*&%$#@!_+={}|<>]", "", text)
    
    # rimozione stopwords, lemmatizzare e mantenere solo parole alfabetiche
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)


with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    current_comment = {} 
    
    for line in infile:
        if line.startswith("Game ID:"):
            current_comment["game_id"] = line.strip().split(": ", 1)[1]
        elif line.startswith("Game Name:"):
            current_comment["game_name"] = line.strip().split(": ", 1)[1]
        elif line.startswith("Comment ID:"):
            current_comment["comment_id"] = line.strip().split(": ", 1)[1]
        elif line.startswith("Comment Text:"):
            raw_text = line.strip().split(": ", 1)[1]
            current_comment["cleaned_text"] = preprocess_comment(raw_text)
        elif line.startswith("Rating:"):
            current_comment["rating"] = line.strip().split(": ", 1)[1]
            
            outfile.write(f"Game ID: {current_comment['game_id']}\n")
            outfile.write(f"Game Name: {current_comment['game_name']}\n")
            outfile.write(f"Comment ID: {current_comment['comment_id']}\n")
            outfile.write(f"Cleaned Comment Text: {current_comment['cleaned_text']}\n")
            outfile.write(f"Rating: {current_comment['rating']}\n")
            outfile.write("-" * 50 + "\n") 

print(f"Commenti puliti salvati in {output_path}")
