import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import classification_report, hamming_loss, accuracy_score

# Carica i dati salvati
X = joblib.load('X_tfidf.pkl')
y = joblib.load('y_labels.pkl')

# Dividi i dati in training e test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inizializza Logistic Regression
base_classifier = LogisticRegression(max_iter=1000)
multi_label_model = MultiOutputClassifier(base_classifier)

# Addestra il modello
multi_label_model.fit(X_train, y_train)

# Valutazione del modello
y_pred = multi_label_model.predict(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Luck", "Bookkeeping", "Downtime", "Interaction", "Bash_the_leader", "Complicated", "Complex"]))

# Hamming Loss e Accuracy
print("Hamming Loss:", hamming_loss(y_test, y_pred))
print("Accuracy Score:", accuracy_score(y_test, y_pred))