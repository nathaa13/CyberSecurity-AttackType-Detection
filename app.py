import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sklearn
import re
from datetime import datetime
from user_agents import parse




# Charger le modèle et les objets nécessaires pour le prétraitement
with open('DecisionTree_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Charger les colonnes d'entraînement
with open("columns_train.pkl", "rb") as f:
    columns_train = pickle.load(f)




# Charger les noms des colonnes pour le fichier brut (avant preprocessing)
X_raw_columns = pd.read_csv("cybersecurity_attacks.csv").columns.tolist()  # Contient les colonnes brutes

# ------------------- 2️⃣ Interface utilisateur -------------------
st.title("🔍 Cybersecurity Attack Prediction App")
st.write("Upload a CSV file or manually enter raw data to predict attack types.")

# Option : Upload CSV ou Entrée manuelle
option = st.radio("Choose input method:", ("Upload CSV", "Manual Entry"))


def parse_user_agent(user_agent):
    ua = parse(user_agent)
    
    os_family = ua.os.family
    os_version = ua.os.version
    device_family = ua.device.family
    device_brand = ua.device.brand if ua.device.brand else "Unknown"
    device_model = ua.device.model if ua.device.model else "Unknown"
    browser_family = ua.browser.family
    
    return os_family, os_version, device_family, device_brand, device_model, browser_family


# **Fonction de prétraitement**
def preprocess_data(df):
    """ Transforme les données brutes pour correspondre au format de X_train """

    df['Firewall Logs'] = df['Firewall Logs'].fillna('No Log')
    df['Proxy Information'] = df['Proxy Information'].fillna('No Proxy')

    df["Malware Indicators"] = df["Malware Indicators"].fillna("No IoC Detected")
    df["Alerts/Warnings"] = df["Alerts/Warnings"].fillna("No Alert Triggered")
    df["IDS/IPS Alerts"] = df["IDS/IPS Alerts"].fillna("No Alert Data")

    df.drop(columns=['Source IP Address', 'Destination IP Address', 'Source Port','Destination Port', 'Payload Data','User Information','Proxy Information'], inplace=True)


    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    df['Month'] = df['Timestamp'].dt.month
    df['Day'] = df['Timestamp'].dt.day
    df['Year'] = df['Timestamp'].dt.year

    df.drop(columns=['Timestamp'], inplace=True)

    df[['Operating System', 'OS Version', 'Device', 'Device Brand', 'Device Model', 'Browser']] = df['Device Information'].apply(lambda x: pd.Series(parse_user_agent(x)))

    df.drop(columns=['Device Information'], inplace=True)

    df['State'] = df['Geo-location Data'].str.split(',').str[1].str.strip()

    df.drop(columns=['Geo-location Data'], inplace=True)


    df_encoded = pd.get_dummies(df, columns=['Protocol', 'Packet Type', 'Traffic Type',
        'Malware Indicators', 'Alerts/Warnings', 'Attack Signature', 'Action Taken', 'Severity Level',
        'Network Segment', 'Firewall Logs', 'IDS/IPS Alerts', 'Log Source',
        'Month', 'Day', 'Operating System', 'OS Version', 'Device',
        'Device Brand', 'Device Model', 'Browser', 'State'])


    # Ajouter les colonnes manquantes et réordonner les colonnes pour correspondre à l'entraînement
    for col in columns_train:
        if col not in df_encoded.columns:
            df_encoded[col] = 0  # Ajouter la colonne manquante avec des 0

    # S'assurer que l'ordre des colonnes est identique
    df_encoded = df_encoded[columns_train]

    return df_encoded

# ------------------- 3️⃣ Upload CSV -------------------
if option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        user_data = pd.read_csv(uploaded_file)  # Chargement brut
        
        # 🔄 Appliquer le prétraitement
        user_data_processed = preprocess_data(user_data)
        
        # 🎯 Prédictions
        predictions = model.predict(user_data_processed)
        predictions = label_encoder.inverse_transform(predictions)  # Convertir en texte

        # 🔍 Affichage des résultats
        user_data["Predicted Attack Type"] = predictions
        st.write("### 🔍 Predicted Attack Types:")
        st.write(predictions)  # Affiche uniquement la colonne des prédictions


        # ⬇️ Option de téléchargement
        csv_output = user_data.to_csv(index=False).encode('utf-8')
        st.download_button("Download Predictions", csv_output, "predictions.csv", "text/csv")

# ------------------- 4️⃣ Entrée Manuelle -------------------
elif option == "Manual Entry":
    st.write("### Enter raw input values manually:")

    # Créer un dictionnaire pour stocker les entrées utilisateur
    manual_input = {}


    def is_valid_ip(ip):
        """ Vérifie si une chaîne est une adresse IP valide. """
        pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
        return re.match(pattern, ip) is not None


    X_raw_columns.remove("Attack Type")


    # Générer des champs dynamiquement basés sur les colonnes brutes
    for col in X_raw_columns:
        if "timestamp" in col.lower():  # Détection de la colonne Timestamp
            # Utilisation de date_input pour la date et time_input pour l'heure
            date_input = st.date_input(f"{col} - Select Date")
            time_input = st.time_input(f"{col} - Select Time")
            
            # Combiner les valeurs de date et d'heure en un seul objet datetime
            combined_timestamp = datetime.combine(date_input, time_input)
            
            # Formater le timestamp selon le format souhaité
            manual_input[col] = combined_timestamp.strftime("%d/%m/%Y %H:%M:%S")
            
        elif col in ["Source IP Address", "Destination IP Address","Proxy Information"]:  # Détection des colonnes IP
            ip_value = st.text_input(f"{col} (Format: xxx.xxx.xxx.xxx)", "")
            manual_input[col] = ip_value
            
            # # Validation et affichage d'un message d'erreur si l'IP est invalide
            # if ip_value and not is_valid_ip(ip_value):
            #     st.error("🚨 Invalid IP address format! Please enter a valid IP (e.g., 103.216.15.12).")
                
            #     manual_input[col] = ip_value
            
        elif col in ["Protocol"]:  
            options = ["ICMP", "UDP", "TCP"]  
            manual_input[col] = st.selectbox(f"{col}", options)
        
        elif col in ["Packet Type"]:  
            options = ["Data", "Control"]  
            manual_input[col] = st.selectbox(f"{col}", options)

        elif col in ["Traffic Type"]:  
            options = ["HTTP", "DNS","FTP"]  
            manual_input[col] = st.selectbox(f"{col}", options)

        elif "payload data" in col.lower():  
            payload_input = st.text_area(f"{col} (Enter the payload data)", "").strip()
            
            manual_input[col] = payload_input  
            
        elif col in ["Malware Indicators"]:  
            options = ["IoC Detected", "No IoC Detected"] 
            manual_input[col] = st.selectbox(f"{col}", options)

        elif col in ["Alerts/Warnings"]:  
            options = ["Alert Triggered", "No Alert Triggered"]  
            manual_input[col] = st.selectbox(f"{col}", options)


        elif col in ["Attack Signature"]:  
            options = ["Known Pattern A", "Known Pattern B"]  
            manual_input[col] = st.selectbox(f"{col}", options)

        elif col in ["Action Taken"]: 
            options = ["Logged", "Blocked","Ignored"]  
            manual_input[col] = st.selectbox(f"{col}", options)

        elif col in ["Severity Level"]:  
            options = ["Low", "Medium","High"] 
            manual_input[col] = st.selectbox(f"{col}", options)

        elif "user information" in col.lower() or "device information" in col.lower() or "geo-location data" in col.lower():

            payload_input = st.text_input(f"{col} (Enter information)", "").strip()
            
            manual_input[col] = payload_input  # Stocker la valeur entrée
        
        elif col in ["Network Segment"]:  
            options = ["Segment A", "Segment B","Segment C"]  
            manual_input[col] = st.selectbox(f"{col}", options)

        elif col in ["Firewall Logs"]:  
            options = ["Log Data", "No Log Data"]  
            manual_input[col] = st.selectbox(f"{col}", options)

        elif col in ["IDS/IPS Alerts"]:  
            options = ["Alert Data", "No Alert Data"]  
            manual_input[col] = st.selectbox(f"{col}", options)

        elif col in ["Log Source"]:  
            options = ["Server", "Firewall"]  
            manual_input[col] = st.selectbox(f"{col}", options)


        else:  # Colonnes numériques
            manual_input[col] = st.number_input(f"{col}", value=0)

    # **Créer un DataFrame brut**
    user_input_df = pd.DataFrame([manual_input])  # Correspond à un fichier CSV brut

    # **🔄 Appliquer le prétraitement sur ces données brutes**
    user_input_processed = preprocess_data(user_input_df)

    # 🎯 Faire la prédiction
    if st.button("Predict"):
        prediction = model.predict(user_input_processed)
        predicted_attack = label_encoder.inverse_transform(prediction)[0]
        st.write(f"### 🛡️ Predicted Attack Type: **{predicted_attack}**")



#streamlit run app.py