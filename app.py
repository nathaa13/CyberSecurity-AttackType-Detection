from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import pickle
import pandas as pd

# ✅ Dictionnaire associant chaque type d’attaque avec une définition et une vidéo explicative

attack_info = {
    "Intrusion": {
        "definition": "An intrusion is unauthorized access to a computer system.",
        "video_url": "https://www.youtube.com/embed/l-yLEb-MweE"
    },
    "Malware": {
        "definition": "Malware is a malicious software designed to harm a system.",
        "video_url": "https://www.youtube.com/embed/NMYbkzjI5EY"
    },
    "DDoS": {
        "definition": "A DDoS attack overwhelms a server with excessive traffic.",
        "video_url": "https://www.youtube.com/embed/yLbC7G71IyE"
    }
}


# ✅ Création de l'application Flask
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Clé secrète pour la gestion des sessions

# ✅ Configuration pour l'upload de fichiers
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB max

# ✅ Vérifier si l'extension du fichier est autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ✅ Charger le modèle de Machine Learning
with open('DecisionTree_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

with open("columns_train.pkl", "rb") as f:
    columns_train = pickle.load(f)

# ✅ Route pour gérer la saisie manuelle
@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    if 'user' not in session:
        return redirect(url_for('login'))

    try:
        data = {key: request.form[key] for key in request.form}
        df = pd.DataFrame([data])

        for col in columns_train:
            if col not in df.columns:
                df[col] = 0

        df = df[columns_train]

        prediction = model.predict(df)
        predicted_attack = label_encoder.inverse_transform(prediction)[0]

        # ✅ Récupérer la définition et la vidéo
        attack_details = attack_info.get(predicted_attack, {
            "definition": "Aucune information disponible.",
            "video_url": ""
        })

        return render_template('dashboard.html', 
                               prediction=predicted_attack,
                               attack_definition=attack_details["definition"],
                               attack_video=attack_details["video_url"])

    except Exception as e:
        return render_template('dashboard.html', error=str(e))

# ✅ Route pour gérer l'upload d'un fichier CSV et faire la prédiction
@app.route('/predict_csv', methods=['POST'])
def predict_csv():
    global attack_info  # ✅ Déclare attack_info comme une variable globale

    if 'user' not in session:
        return redirect(url_for('login'))

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        try:
            user_data = pd.read_csv(filepath)

            for col in columns_train:
                if col not in user_data.columns:
                    user_data[col] = 0

            user_data = user_data[columns_train]

            predictions = model.predict(user_data)
            predictions = label_encoder.inverse_transform(predictions)

            # ✅ Associer chaque attaque avec sa définition et vidéo
            attack_results = [
                {
                    "attack": pred,
                    "definition": attack_info.get(pred, {}).get("definition", "Aucune information disponible."),
                    "video_url": attack_info.get(pred, {}).get("video_url", "")
                }
                for pred in predictions
            ]

            return render_template('dashboard.html', attack_results=attack_results)

        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500

    return jsonify({"error": "File type not allowed"}), 403

# ✅ Page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Page "À propos"
@app.route('/about')
def about():
    return render_template('about.html')

# ✅ Page "Contact"
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ✅ Page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "ANASKA" and password == "cyberA24":
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="❌ Identifiants incorrects !")

    return render_template('login.html')

# ✅ Route pour déconnexion
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ✅ Route pour afficher le Dashboard Flask
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')

if __name__ == '__main__':
    # ✅ Vérifier que le dossier d'upload existe
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True)

# ✅ Mapping each attack type with its definition and explanatory video
attack_info = {
    "Intrusion": {
        "definition": "An intrusion is unauthorized access to a computer system.",
        "video_url": "https://www.youtube.com/embed/l-yLEb-MweE"
    },
    "Malware": {
        "definition": "Malware is a malicious software designed to harm a system.",
        "video_url": "https://www.youtube.com/embed/NMYbkzjI5EY"
    },
    "DDoS": {
        "definition": "A DDoS attack overwhelms a server with excessive traffic.",
        "video_url": "https://www.youtube.com/embed/yLbC7G71IyE"
    }
}
