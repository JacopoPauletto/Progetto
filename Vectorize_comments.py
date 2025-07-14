from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import joblib

# Carica il file dei commenti etichettati
labeled_comments_path = 'D:\\natural lenguages\\progetto\\labeled_comments.txt'

# Caricamento dei dati
comments = []
labels = []

# Parsing del file etichettato
with open(labeled_comments_path, 'r', encoding='utf-8') as file:
    current_comment = {}
    for line in file:
        if ": " in line:
            key, value = line.strip().split(": ", 1)
            if key == "Cleaned Comment Text":
                current_comment["text"] = value
            elif key in ["Luck", "Bookkeeping", "Downtime", "Interaction", "Bash_the_leader", "Complicated", "Complex"]:
                if "labels" not in current_comment:
                    current_comment["labels"] = []
                current_comment["labels"].append(int(value))
        elif line.strip() == "-" * 50:
            # Salva il commento ed etichette
            comments.append(current_comment["text"])
            labels.append(current_comment["labels"])
            current_comment = {}

# Vettorizza i commenti con TF-IDF
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(comments)

# Converti le etichette in un array
import numpy as np
y = np.array(labels)

# Salva X e y
joblib.dump(X, 'X_tfidf.pkl')
joblib.dump(y, 'y_labels.pkl')

print(f"Shape di X: {X.shape}")
print(f"Shape di y: {y.shape}")
print("Dati salvati con successo.")
