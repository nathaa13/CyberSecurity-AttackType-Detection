# Cybersecurity Attack Type Prediction App

This application predicts the type of attack based on provided information (Timestamp, Destination IP Address, Source Port, Protocol, etc.). It is built with **Flask** and uses a selected prediction model trained on a dataset of 40,000 observations.


## 🔧 Prerequisites

Before running the application, make sure you have the following software installed on your machine:

1. **Git**: to clone the project  
   -  📥 [Download Git](https://git-scm.com/downloads)
   - Verify the installation with the command:
     ```bash
     git --version
     ```

2. **Python 3.12.4** 
   - 📥 [Download Python 3.12.4](https://www.python.org/downloads/release/python-3124/)  
   - Check if Python is already installed with:
     ```bash
     python --version
     ```

---

## 📥 Installation and Setup

### 1️⃣ Clone the project repository

Open a terminal and run the following command to retrieve the project from the GitHub repository:

```bash
git clone https://github.com/nathaa13/CyberSecurity-AttackType-Detection.git
```

Then, navigate to the project directory:

```bash
cd CyberSecurity-AttackType-Detection
```

### 2️⃣ Create a virtual environment with `venv`

Create a new virtual environment in the project directory, named "cybersec_env" (or another name of your choice):

```bash
python -m venv cybersec_env
```

Activate the environment:

```bash
cybersec_env\Scripts\activate
```


### 3️⃣ Install dependencies

With the environment activated, install the required libraries using `pip` :

```bash
pip install -r requirements.txt
```

---


## 📂 Required Files

The application requires certain .pkl files to function properly.

Make sure you have the following files in the project directory (at the same level as app.py):

- `DecisionTree_model.pkl`   -> Prediction model
- `columns_train.pkl`        -> For data preprocessing
- `label_encoder.pkl`        -> For data preprocessing

⚠️  If these files are missing, the application will not be able to make predictions.

---

## 🚀 Run the Application

Once all dependencies are installed and the .pkl files are in place, run the following command to start the application:

```bash
python app.py
```

This will automatically open the application in your default browser. If not, copy and paste the URL displayed in your browser.

---

## 🎯 How to Use the Application

Go to the "Login" page and enter "ANASKA" as the username and "cyberA24" as the password

The application allows predicting the type of cybersecurity attack in two ways:

### 📝 1️⃣ Manual Prediction
* Enter the required information through the user interface.
* Click **"Predict"** to get the predicted attack type.

### 📂 2️⃣ Prediction from a CSV File
* Click the **"Browse files"** button to upload a CSV file.
* The file must follow the format of the original cybersecurity_attacks dataset (**without the "Attack Type" column**). Examples of CSV files to provide in testpredict.csv and testpredict-several-lines.csv.
* The application will display predictions for each row in the file.

The result will be displayed at the bottom of the page!

