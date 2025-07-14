import re

# Percorso dei file di input e output
input_path = 'D:\\natural lenguages\\progetto\\cleaned_comments.txt'
output_path = 'D:\\natural lenguages\\progetto\\labeled_comments.txt'

# Definisci le parole chiave per ciascuna etichetta
keywords = {
    "luck": [
        r"\b(luck|random|chance|alea|rolls?|dice|fortune|unpredictable)\b",
        r"\b(not in control|no control|out of control|beyond control)\b",
        r"\b(outcome|result|game\s*outcome) (is )?random\b"
    ],
    "bookkeeping": [
        r"\b(bookkeeping|record\s*(keeping|tracking)|data\s*tracking|data\s*recording|manual\s*entry)\b",
        r"\b(reference(s)?\s*(the\s*)?(rules?|rulebook|booklet|manual)|check(s|ing)?\s*(the\s*)?(rules?|rulebook|manual))\b",
        r"\b(rulebook|manual|booklet)\s*(is\s*(bad|awful|poor|terrible|confusing|hard\s*to\s*follow))\b",
        r"\b(update\s*(parameters|values|stats|numbers|scores|counters))\b",
        r"\b(manual\s*(calculation|tracking|entry|updating))\b",
        r"\b(continual\s*updating|frequent\s*updates|constant\s*adjustments)\b",
        r"\b(game\s*flow\s*interrupted|manual\s*data\s*entry|tracking\s*slows\s*down\s*gameplay)\b",
        r"\b(spending\s*too\s*much\s*time\s*tracking|having\s*to\s*write\s*down\s*data)\b",
        r"\b(feels\s*like\s*a\s*chore|unnecessary\s*steps|too\s*many\s*adjustments)\b",
        r"\b(not\s*engaging|adds\s*no\s*value|not\s*fun|tedious\s*task|boring\s*task)\b",
        r"\b(video\s*game\s*comparison|AI\s*does\s*this|should\s*be\s*automatic|automatically\s*calculated)\b",
        r"\b(prone\s*to\s*error|easy\s*to\s*make\s*mistakes|complicated\s*to\s*track)\b",
        r"\b(difficult\s*bookkeeping|hard\s*to\s*follow|leads\s*to\s*errors)\b",
        r"\b(rulebook\s*(is|was)?\s*(confusing|annoying|bad|poor|difficult|frustrating))\b",
        r"\b(checking\s*(rules?|rulebook|manual|instructions|guide)\s*(too\s*much|constantly|repeatedly))\b"
    ],
    "downtime": [
        r"\b(downtime|waiting\s*time|wait\s*time|idle\s*time|standby|lag\s*time)\b",
        r"\b(nothing (to )?do|bored|not engaged|no (thinking|strategy))\b",
        r"\b(turn\s*waiting|wait\s*for turn|unproductive)\b",
        r"\b(long (turn|pause|break|delay))\b",
        r"\b(boredom|time\s*wasting|waste (of )?time)\b"
    ],
    "interaction": [
        r"\b(interaction|interactivity|interact(s|ed|ing)?|player\s*interaction)\b",
        r"\b(player\s*influence|impact\s*other\s*players|mutual\s*influence)\b",
        r"\b(direct\s*interaction|affect\s*others|player\s*conflict)\b",
        r"\b(cross\s*play|opponent\s*interference|actions\s*impact\s*others)\b"
    ],
    "bash_the_leader": [
        r"\b(bookkeeping|record\s*(keeping|tracking)|data\s*tracking|data\s*recording|manual\s*entry)\b",
        r"\b(update\s*(parameters|values|stats)|manual\s*(calculation|tracking))\b",
        r"\b(continual\s*updating|frequent\s*updates|constant\s*adjustments)\b",
        r"\b(referencing\s*rules|checking\s*rulebook|rule\s*lookup|rule\s*reference)\b",
        r"\b(spending\s*too\s*much\s*time\s*tracking|having\s*to\s*write\s*down\s*data)\b",
        r"\b(game\s*flow\s*interrupted\s*by\s*record\s*keeping)\b",
        r"\b(feels\s*like\s*a\s*chore|unnecessary\s*steps|too\s*many\s*adjustments)\b",
        r"\b(not\s*engaging|adds\s*no\s*value|not\s*fun|tedious\s*task)\b",
        r"\b(video\s*game\s*comparison|AI\s*does\s*this|should\s*be\s*automatic|automatically\s*calculated)\b",
        r"\b(prone\s*to\s*error|easy\s*to\s*make\s*mistakes|complicated\s*to\s*track)\b",
        r"\b(difficult\s*bookkeeping|hard\s*to\s*follow|leads\s*to\s*errors)\b"
    ],
    "complicated": [
        r"\b(complicated|complex\s*rules|difficult\s*to\s*learn|hard\s*to\s*grasp)\b",
        r"\b(many\s*rules|lots\s*of\s*exceptions|too\s*many\s*variables)\b",
        r"\b(rule\s*exceptions|exception\s*to\s*rules|specific\s*rules)\b",
        r"\b(overly\s*complicated|difficult\s*to\s*understand|intricate)\b"
    ],
    "complex": [
        r"\b(complex|deep\s*strategy|hard\s*to\s*master|requires\s*skill)\b",
        r"\b(cause\s*more\s*problems|new\s*challenges|multiple\s*outcomes)\b",
        r"\b(requires\s*foresight|many\s*layers|difficult\s*to\s*anticipate)\b",
        r"\b(challenging\s*gameplay|strategic\s*depth|unpredictable\s*results)\b"
    ]
}


def label_comment(text, keywords):
    labels = {}
    for label, patterns in keywords.items():
        matched_keywords = [pattern for pattern in patterns if re.search(pattern, text, re.IGNORECASE)]
        if matched_keywords:
            labels[label] = 1
            print(f"Matched {label}: {matched_keywords} in comment: {text}")
        else:
            labels[label] = 0
    return labels

# Elabora il file riga per riga e applica le etichette
with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    current_comment = {}
    
    for line in infile:
        if ": " in line:
            try:
                key, value = line.strip().split(": ", 1)
                if key == "Game ID":
                    current_comment["game_id"] = value
                elif key == "Game Name":
                    current_comment["game_name"] = value
                elif key == "Comment ID":
                    current_comment["comment_id"] = value
                elif key == "Cleaned Comment Text":
                    current_comment["cleaned_text"] = value
                elif key == "Rating":
                    current_comment["rating"] = value
            except ValueError:
                print(f"Errore nel processare la riga: {line.strip()}")
        elif line.strip() == "-" * 50:  # Fine di un commento
            if "cleaned_text" in current_comment:
                # Ignora commenti vuoti o troppo brevi
                if not current_comment["cleaned_text"] or len(current_comment["cleaned_text"].split()) < 3:
                    print(f"Commento troppo breve o vuoto, ignorato: {current_comment['cleaned_text']}")
                    current_comment = {}
                    continue
                
                # Etichetta il commento
                labels = label_comment(current_comment["cleaned_text"], keywords)
                
                # Scrivi i dati e le etichette nel file di output
                outfile.write(f"Game ID: {current_comment['game_id']}\n")
                outfile.write(f"Game Name: {current_comment['game_name']}\n")
                outfile.write(f"Comment ID: {current_comment['comment_id']}\n")
                outfile.write(f"Cleaned Comment Text: {current_comment['cleaned_text']}\n")
                outfile.write(f"Rating: {current_comment['rating']}\n")
                for label, value in labels.items():
                    outfile.write(f"{label.capitalize()}: {value}\n")
                outfile.write("-" * 50 + "\n")
            
            current_comment = {}

print(f"Commenti etichettati salvati in {output_path}")

