# === CONFIGURAZIONE ===
input_path = "D:\\natural lenguages\\progetto\\labeled_comments.txt"

# Etichette da controllare
all_labels = ["Luck", "Bookkeeping", "Downtime", "Interaction", "Bash_the_leader", "Complicated", "Complex"]

# === STEP 1: CARICAMENTO DEI DATI ===
print("Caricamento dei dati...")

comments_with_labels = 0
total_comments = 0

with open(input_path, 'r', encoding='utf-8') as file:
    current_comment_has_label = False  # Flag per il commento in corso

    for line in file:
        if ": " in line:
            key, value = line.strip().split(": ", 1)

            # Se la chiave è un'etichetta e ha valore 1, segna il commento come valido
            if key in all_labels and value == "1":
                current_comment_has_label = True

        elif line.strip() == "-" * 50:  # Quando troviamo il separatore, significa che il commento è finito
            total_comments += 1
            if current_comment_has_label:
                comments_with_labels += 1
            current_comment_has_label = False  # Reset per il prossimo commento

# === STEP 2: STAMPA RISULTATI ===
print(f"Numero totale di commenti: {total_comments}")
print(f"Numero di commenti con almeno un'etichetta: {comments_with_labels}")
