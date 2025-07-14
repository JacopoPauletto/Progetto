import re

bookkeeping_keywords = [
    # Termini principali di bookkeeping
    r"\b(bookkeeping|record\s*(keeping|tracking)|data\s*tracking|data\s*recording|manual\s*entry)\b",
    
    # Consultazione del rulebook e problemi legati alle regole
    r"\b(reference(s)?\s*(the\s*)?(rules?|rulebook|booklet|manual)|check(s|ing)?\s*(the\s*)?(rules?|rulebook|manual))\b",
    r"\b(rulebook|manual|booklet)\s*(is\s*(bad|awful|poor|terrible|confusing|hard\s*to\s*follow))\b",
    
    # Aggiornamento costante di parametri e valori
    r"\b(update\s*(parameters|values|stats|numbers|scores|counters))\b",
    r"\b(manual\s*(calculation|tracking|entry|updating))\b",
    r"\b(continual\s*updating|frequent\s*updates|constant\s*adjustments)\b",
    
    # Interruzione del flusso di gioco a causa del bookkeeping
    r"\b(game\s*flow\s*interrupted|manual\s*data\s*entry|tracking\s*slows\s*down\s*gameplay)\b",
    r"\b(spending\s*too\s*much\s*time\s*tracking|having\s*to\s*write\s*down\s*data)\b",

    # Frustrazione e noia associata al bookkeeping
    r"\b(feels\s*like\s*a\s*chore|unnecessary\s*steps|too\s*many\s*adjustments)\b",
    r"\b(not\s*engaging|adds\s*no\s*value|not\s*fun|tedious\s*task|boring\s*task)\b",
    
    # Confronto con i videogiochi (bookkeeping automatizzabile)
    r"\b(video\s*game\s*comparison|AI\s*does\s*this|should\s*be\s*automatic|automatically\s*calculated)\b",
    
    # Problemi di errori nel bookkeeping
    r"\b(prone\s*to\s*error|easy\s*to\s*make\s*mistakes|complicated\s*to\s*track)\b",
    r"\b(difficult\s*bookkeeping|hard\s*to\s*follow|leads\s*to\s*errors)\b"
]

test_comments = [
    "I hate the bookkeeping in this game, it's so tedious!",
    "The rulebook is awful, I have to check it all the time.",
    "This game is just a boring task of updating values.",
    "It's like a video game where the AI should handle all this bookkeeping!",
    "The game flow is constantly interrupted by all this manual data entry."
]

for comment in test_comments:
    match = any(re.search(pattern, comment, re.IGNORECASE) for pattern in bookkeeping_keywords)
    print(f"'{comment}' → {'MATCH' if match else 'NO MATCH'}")
