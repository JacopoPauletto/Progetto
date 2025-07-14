import torch
import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel, BertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, hamming_loss
from sklearn.preprocessing import MultiLabelBinarizer
from torch.utils.data import Dataset, DataLoader
from torch import nn, optim

print("CUDA disponibile:", torch.cuda.is_available())
print("Versione CUDA:", torch.version.cuda)
print("Numero di GPU:", torch.cuda.device_count())
print("Nome GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Nessuna GPU trovata")

# === CONFIGURAZIONE ===
input_path = "D:\\natural lenguages\\progetto\\labeled_comments.txt"
output_path = "D:\\natural lenguages\\progetto\\bert_results.txt"
pretrained_model = "bert-base-uncased"
batch_size = 8
epochs = 5
learning_rate = 2e-5

# === STEP 1: CARICAMENTO DEI DATI ===
print("Caricamento dei dati...")
comments = []
labels = []
all_labels = ["Luck", "Bookkeeping", "Downtime", "Interaction", "Bash_the_leader", "Complicated", "Complex"]

with open(input_path, 'r', encoding='utf-8') as file:
    current_comment = {}
    for line in file:
        if ": " in line:
            key, value = line.strip().split(": ", 1)
            if key == "Cleaned Comment Text":
                current_comment["text"] = value
            elif key in all_labels:
                if "labels" not in current_comment:
                    current_comment["labels"] = []
                if int(value) == 1:
                    current_comment["labels"].append(key)
        elif line.strip() == "-" * 50:
            comments.append(current_comment["text"])
            labels.append(current_comment["labels"])
            current_comment = {}

print(f"Numero di commenti: {len(comments)}")

# === STEP 2: TOKENIZZAZIONE CON BERT ===
print("Tokenizzazione con BERT...")
tokenizer = BertTokenizer.from_pretrained(pretrained_model)

mlb = MultiLabelBinarizer(classes=all_labels)
y = mlb.fit_transform(labels)

X_train, X_test, y_train, y_test = train_test_split(comments, y, test_size=0.2, random_state=42)

# === CREAZIONE DATASET COMPATIBILE CON PyTorch ===
class CommentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        text = self.texts[index]
        labels = torch.tensor(self.labels[index], dtype=torch.float)
        encoding = self.tokenizer(
            text,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": labels,
        }

train_dataset = CommentDataset(X_train, y_train, tokenizer)
test_dataset = CommentDataset(X_test, y_test, tokenizer)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

# === COSTRUZIONE DEL MODELLO ===
class MultiLabelBERT(nn.Module):
    def __init__(self, pretrained_model, num_labels):
        super(MultiLabelBERT, self).__init__()
        self.bert = BertModel.from_pretrained(pretrained_model)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        logits = self.classifier(outputs.pooler_output)
        return self.sigmoid(logits)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MultiLabelBERT(pretrained_model, num_labels=len(all_labels)).to(device)
print(f"🔹 Training su: {device}")
model.to(device)

# === DEFINIZIONE DI PERDITA E OTTIMIZZATORE ===
criterion = nn.BCELoss()
optimizer = optim.AdamW(model.parameters(), lr=learning_rate)

# === TRAINING DEL MODELLO ===
print("Inizio addestramento...")
for epoch in range(epochs):
    model.train()
    total_loss = 0
    print(f"🔹 Epoch {epoch + 1}/{epochs} in corso...")

    for batch_idx, batch in enumerate(train_loader):
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        # Debug: Stampa le dimensioni dei tensori
        if batch_idx == 0:
            print(f"📌 Batch {batch_idx}: input_ids {input_ids.shape}, labels {labels.shape}")

        optimizer.zero_grad()
        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

        # Debug: Stampa ogni 100 batch
        if batch_idx % 100 == 0:
            print(f"✅ Epoch {epoch + 1}, Batch {batch_idx}/{len(train_loader)} - Loss: {loss.item():.4f}")

    print(f"🎯 Epoch {epoch + 1} completata - Loss media: {total_loss / len(train_loader):.4f}")

# === VALUTAZIONE DEL MODELLO ===
print("Valutazione del modello...")
model.eval()
y_pred_list = []

with torch.no_grad():
    for batch in test_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(input_ids, attention_mask)
        y_pred_list.append(outputs.cpu().numpy())

y_pred = np.vstack(y_pred_list)
y_pred_bin = (y_pred > 0.5).astype(int)  # Ottimizzabile con soglia personalizzata

for i in range(10):  # Controlliamo i primi 10 esempi
    print(f"y_test[{i}]: {y_test[i]}")
    print(f"y_pred[{i}]: {y_pred[i]}")

# Contiamo il numero medio di etichette per commento
print(f"Numero medio di etichette per commento in y_test: {np.mean(np.sum(y_test, axis=1))}")
print(f"Numero medio di etichette per commento in y_pred: {np.mean(np.sum(y_pred, axis=1))}")

# === METRICHE DI VALUTAZIONE ===
report = classification_report(y_test, y_pred_bin, target_names=mlb.classes_)
print(report)

print("Hamming Loss:", hamming_loss(y_test, y_pred_bin))
print("Accuracy Score:", accuracy_score(y_test, y_pred_bin))


# === SALVATAGGIO DEI RISULTATI ===
print("Salvataggio dei risultati...")
with open(output_path, "w", encoding="utf-8") as output_file:
    output_file.write("=== REPORT DI CLASSIFICAZIONE ===\n")
    output_file.write(report)

torch.save(model.state_dict(), "D:\\natural lenguages\\progetto\\bert_model.pth")

print(f"Risultati salvati in {output_path}")


