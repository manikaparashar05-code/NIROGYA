# 🧬 NIROGYA — AI-Powered Disease Risk & Health Analytics

> An intelligent healthcare analytics platform that uses **Data Mining, Machine Learning, and Explainable AI** to discover disease-related patterns, analyze patient data, and estimate disease risk.

---

## 📌 Overview

**NIROGYA** is an AI-powered healthcare analytics platform designed to analyze patient health data and discover meaningful patterns related to disease risk.

The project combines multiple **Data Mining and Machine Learning techniques** rather than relying on a single prediction model.

NIROGYA aims to provide:

* Disease risk prediction
* Healthcare data analysis
* Patient clustering
* Association rule mining
* Anomaly detection
* Explainable predictions
* Interactive healthcare analytics

> **Note:** NIROGYA is an educational and research project and is not intended to provide medical diagnosis or replace professional medical advice.

---

## 🎯 Objectives

The major objectives of NIROGYA are:

* Analyze healthcare datasets to identify important patterns.
* Discover relationships between different health attributes.
* Predict potential disease risk using machine learning.
* Segment patients based on similar health characteristics.
* Identify unusual or anomalous patient records.
* Generate association rules from healthcare data.
* Provide interpretable insights behind predictions.
* Present healthcare insights through an interactive dashboard.

---

## 🔍 Key Features

### 🩺 Disease Risk Prediction

Uses machine learning classification algorithms to estimate disease risk based on patient health attributes.

Potential inputs include:

* Age
* Gender
* BMI
* Blood glucose
* Blood pressure
* Cholesterol
* Heart rate
* Lifestyle factors
* Other relevant clinical attributes

---

### ⛏️ Data Mining & Pattern Discovery

NIROGYA applies data mining techniques to discover hidden patterns and relationships within healthcare data.

---

### 👥 Patient Clustering

Uses clustering techniques such as **K-Means** to group patients with similar health profiles.

Example groups:

* Low-risk profiles
* Moderate-risk profiles
* High-risk profiles

---

### 🔗 Association Rule Mining

Uses techniques such as **Apriori / FP-Growth** to discover relationships between healthcare attributes.

Example:

> High BMI + Elevated Glucose → frequently associated with higher diabetes risk.

The discovered rules can be evaluated using:

* Support
* Confidence
* Lift

---

### 🚨 Anomaly Detection

Identifies unusual patient records or abnormal combinations of health attributes using anomaly detection techniques.

Potential algorithms include:

* Isolation Forest
* DBSCAN

---

### 🧠 Explainable AI

NIROGYA aims to provide explanations behind predictions instead of displaying only a risk score.

Example:

**Major contributing factors:**

* Elevated glucose
* High BMI
* Increased blood pressure
* Age-related risk

---

### 📊 Interactive Healthcare Dashboard

The dashboard can display:

* Disease distribution
* Patient risk categories
* Important risk factors
* Correlation analysis
* Patient clusters
* Association rules
* Anomalies
* Prediction results

---

## 🏗️ Project Architecture

```text
                ┌──────────────────────┐
                │     Patient Data     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   Data Preprocessing │
                │ Cleaning & Transform │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Data Mining       │
                ├──────────────────────┤
                │ Classification       │
                │ Clustering           │
                │ Association Mining   │
                │ Anomaly Detection    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Explainable Analysis │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Healthcare Dashboard │
                └──────────────────────┘
```

---

## 🧪 Data Mining Techniques

| Technique                 | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| Data Preprocessing        | Clean and prepare healthcare data          |
| Exploratory Data Analysis | Understand distributions and relationships |
| Classification            | Disease risk prediction                    |
| Clustering                | Patient segmentation                       |
| Association Rule Mining   | Discover healthcare patterns               |
| Anomaly Detection         | Identify unusual records                   |
| Feature Selection         | Identify important risk factors            |

---

## 🛠️ Technology Stack

### Programming

* Python

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-learn

### Data Mining

* MLxtend

### Visualization

* Matplotlib
* Plotly

### Explainable AI

* SHAP

### Backend

* FastAPI

### Database

* MySQL

### Dashboard

* Streamlit

### Development

* VS Code
* Git & GitHub

---

## 📁 Project Structure

```text
NIROGYA/
│
├── backend/
│
├── frontend/
│
├── data/
│
├── models/
│
├── notebooks/
│
├── src/
│   ├── preprocessing.py
│   ├── prediction.py
│   ├── clustering.py
│   ├── association_rules.py
│   └── anomaly_detection.py
│
├── database/
│
├── requirements.txt
├── README.md
└── .gitignore
```

> Project structure may evolve as new modules are implemented.

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/NIROGYA.git
```

### 2. Navigate to the project

```bash
cd NIROGYA
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows:**

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the database

Create the required MySQL database and configure the database connection through environment variables.

---

## 🚀 Future Scope

NIROGYA can be further extended with:

* Multi-disease prediction
* Real-time health monitoring
* Wearable-device integration
* Larger healthcare datasets
* Advanced deep learning models
* Personalized health recommendations
* Cloud deployment
* Mobile application
* Federated learning for privacy-preserving healthcare analytics

---

## 🔐 Privacy & Security

Healthcare data is sensitive. The project is designed with security considerations such as:

* Authentication
* Password hashing
* Input validation
* Restricted access to patient information
* Secure database practices
* Avoiding exposure of sensitive credentials

No real patient information should be used without appropriate authorization and privacy safeguards.

---

## 📈 Project Status

🚧 **Currently Under Development**

Planned development stages:

* [x] Initial project setup
* [x] Healthcare dataset integration
* [ ] Data preprocessing pipeline
* [ ] Exploratory data analysis
* [ ] Disease risk prediction
* [ ] Patient clustering
* [ ] Association rule mining
* [ ] Anomaly detection
* [ ] Explainable AI
* [ ] Interactive dashboard
* [ ] API integration
* [ ] Authentication
* [ ] Deployment

---

## 👩‍💻 Author

**Manika Parashar**

B.Tech — Computer Science & Artificial Intelligence

---

## ⚠️ Disclaimer

NIROGYA is developed for **educational, academic, and research purposes**.

The predictions and analytics generated by this system should not be considered a medical diagnosis or a substitute for consultation with a qualified healthcare professional.
