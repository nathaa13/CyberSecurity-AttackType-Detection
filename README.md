# Cybersecurity Attack Type Prediction App

Cette application permet de prédire le type d'attaque à partir d'informations fournis (Timestamp, Destination IP Address, Source Port, Protocol..). Elle est construite avec **Streamlit** et utilise un modèle de prédiction sélectionné, qui a été entraîné sur un dataset de 40000 observations.

## 🔧 Prérequis

Avant de pouvoir exécuter l'application, assurez-vous d'avoir les logiciels suivants installés sur votre machine:

1. **Git** : pour cloner le projet  
   - 📥 [Télécharger Git](https://git-scm.com/downloads)  
   - Vérifier l'installation avec la commande :
     ```bash
     git --version
     ```

2. **Python 3.12.4** 
   - 📥 [Télécharger Python 3.12.4](https://www.python.org/downloads/release/python-3124/)  
   - Vérifier si Python est déjà installé avec :
     ```bash
     python --version
     ```

---

## 📥 Installation et configuration

### 1️⃣ Cloner le répertoire du projet

Ouvrez un terminal et exécutez la commande suivante pour récupérer le projet depuis le dépôt GitHub :

```bash
git clone https://github.com/nathaa13/CyberSecurity-AttackType-Detection.git
```


Accédez ensuite au répertoire du projet :

```bash
cd nom_du_projet
```

### 2️⃣ Créer un environnement virtuel avec `venv`
Créez un nouvel environnement virtuel dans le répertoire de votre projet, nommé "cybersec_env" (ou un autre nom de votre choix) :

```bash
python -m venv cybersec_env
```
Activez l’environnement :

```bash
cybersec_env\Scripts\activate
```
### 3️⃣ Installer les dépendances
Dans l'environnement activé, installez les bibliothèques requises via `pip` :

```bash
pip install -r requirements.txt
```

---


## 📂 Fichiers nécessaires
L'application nécessite certains fichiers .pkl pour fonctionner correctement.

Assurez-vous d’avoir les fichiers suivants dans le répertoire du projet (au même niveau que app.py) :

* `DecisionTree_model.pkl` (modèle de prédiction)
* `columns_train.pkl` (pour le prétraitement des données)
* `label_encoder.pkl` (pour le prétraitement des données)
⚠️ Si ces fichiers ne sont pas fournis, l'application ne pourra pas effectuer de prédictions.

---

## 🚀 Lancer l'application
Une fois toutes les dépendances installées et les fichiers .pkl en place, exécutez la commande suivante pour démarrer l’application :

```bash
streamlit run app.py
```
Cela ouvrira automatiquement l'application dans votre navigateur par défaut.

---

## 🎯 Utilisation de l'application
L'application permet de prédire le type d'attaque en cybersécurité de deux manières :

### 📝 1️⃣ Prédiction manuelle
* Entrez les informations requises via l'interface utilisateur.
* Cliquez sur "Prédire" pour obtenir le type d'attaque prédit.
### 📂 2️⃣ Prédiction à partir d'un fichier CSV
* Cliquez sur le bouton "Browse files" pour charger un fichier de données au format CSV.
* Le fichier doit respecter le format du dataset d'entraînement du modèle. (sans la colonne "Attack Type")
* L'application affichera les prédictions pour chaque ligne du fichier.
