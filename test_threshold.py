import torch
import numpy as np
import matplotlib.pyplot as plt
from transformers import BertTokenizer, BertModel
from torch.utils.data import DataLoader, Dataset
from sklearn.metrics import classification_report, accuracy_score, hamming_loss, precision_score, recall_score
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split

input_path = "D:\\natural lenguages\\progetto\\labeled_comments.txt"
model_path = "D:\\natural lenguages\\progetto\\bert_model.pth"
pretrained_model = "bert-base-uncased"
batch_size = 8
all_labels = ["Luck", "Bookkeeping", "Downtime", "Interaction", "Bash_the_leader", "Complicated", "Complex"]


print("Caricamento dei dati")
comments, labels = [], []

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

mlb = MultiLabelBinarizer(classes=all_labels)
y = mlb.fit_transform(labels)

X_train, X_test, y_train, y_test = train_test_split(comments, y, test_size=0.2, random_state=42)

num_labeled_comments = np.sum(np.sum(y_test, axis=1) > 0)
print(f"Numero di commenti con almeno un'etichetta in y_test: {num_labeled_comments}")

print("Supporto:", np.sum(y_test))

num_multi_label_comments = np.sum(np.sum(y_test, axis=1) > 1)
print(f"Numero di commenti con più di un'etichetta: {num_multi_label_comments}")

print("Tokenizzazione con BERT...")
tokenizer = BertTokenizer.from_pretrained(pretrained_model)

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

test_dataset = CommentDataset(X_test, y_test, tokenizer)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

class MultiLabelBERT(torch.nn.Module):
    def __init__(self, pretrained_model, num_labels):
        super(MultiLabelBERT, self).__init__()
        self.bert = BertModel.from_pretrained(pretrained_model)
        self.classifier = torch.nn.Linear(self.bert.config.hidden_size, num_labels)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        logits = self.classifier(outputs.pooler_output)
        return self.sigmoid(logits)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Test su: {device}")

model = MultiLabelBERT(pretrained_model, num_labels=len(all_labels)).to(device)
model.load_state_dict(torch.load(model_path, map_location=device))
model.eval()

y_pred_list = []

with torch.no_grad():
    for batch in test_loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        outputs = model(input_ids, attention_mask)
        y_pred_list.append(outputs.cpu().numpy())

y_pred = np.vstack(y_pred_list)

thresholds = np.linspace(0.1, 0.9, 9)
precision_scores, recall_scores, f1_scores = [], [], []
best_threshold, best_f1 = 0.5, 0 

print("Ricerca della soglia")
for t in thresholds:
    y_pred_bin = (y_pred > t).astype(int)
    precision = precision_score(y_test, y_pred_bin, average="micro")
    recall = recall_score(y_test, y_pred_bin, average="micro")
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)

    if f1 > best_f1:
        best_f1, best_threshold = f1, t

print(f"Soglia ottimale: {best_threshold:.2f} con F1-score {best_f1:.4f}")

y_pred_bin = (y_pred > best_threshold).astype(int)

print("REPORT DI CLASSIFICAZIONE")
report = classification_report(y_test, y_pred_bin, target_names=mlb.classes_)
print(report)

print("Hamming Loss:", hamming_loss(y_test, y_pred_bin))
print("Accuracy Score:", accuracy_score(y_test, y_pred_bin))

plt.figure(figsize=(8, 6))
plt.plot(thresholds, precision_scores, marker='o', label="Precision", linestyle='-')
plt.plot(thresholds, recall_scores, marker='s', label="Recall", linestyle='-')
plt.plot(thresholds, f1_scores, marker='x', label="F1-score", linestyle='-')
plt.xlabel("Threshold")
plt.ylabel("Score")
plt.title("Precision-Recall-F1 vs. Threshold")
plt.legend()
plt.grid()
plt.savefig("threshold_analysis.png")
plt.show()

print("Grafico salvato")
