from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import joblib

labeled_comments_path = 'D:\\natural lenguages\\progetto\\labeled_comments.txt'

comments = []
labels = []


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
            comments.append(current_comment["text"])
            labels.append(current_comment["labels"])
            current_comment = {}

vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(comments)


import numpy as np
y = np.array(labels)

joblib.dump(X, 'X_tfidf.pkl')
joblib.dump(y, 'y_labels.pkl')

print(f"Shape di X: {X.shape}")
print(f"Shape di y: {y.shape}")
print("Dati salvati con successo.")
