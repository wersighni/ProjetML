import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'random_forest_model.pkl')

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        "❌ Modèle ML manquant. Veuillez télécharger le fichier random_forest_model.pkl "
        "et le placer dans predictor/"
    )
model = joblib.load(MODEL_PATH)

FEATURES = [
    'Age',
    'Gender_M',
    'Gender_F',
    'Billing Amount',
    'Stay_Duration',
    'Medical Condition_Cardiology',
    'Medical Condition_Neurology',
    'Medical Condition_Cancer',
    'Medical Condition_Trauma',
    'Medical Condition_Others',
    'Admission Type_Emergency',
    'Admission Type_Urgent',
    'Admission Type_Routine',
    'Insurance_Private',
    'Insurance_Gov',
    'Insurance_None',
    'Test_Result_Positive',
    'Test_Result_Negative'
]

def build_input(data):
    x = {c: 0 for c in FEATURES}

    x['Age'] = data['age']
    x['Billing Amount'] = data['billing']

  
    x['Stay_Duration'] = (data['discharge_date'] - data['admission_date']).days

    x['Gender_' + ('M' if data['gender'] == 'M' else 'F')] = 1

  
    m = "Medical Condition_" + data['medical_condition']
    if m in x:
        x[m] = 1

  
    a = "Admission Type_" + data['admission_type']
    if a in x:
        x[a] = 1

  
    i = "Insurance_" + data['insurance']
    if i in x:
        x[i] = 1

   
    t = "Test_Result_" + data['test_results']
    if t in x:
        x[t] = 1

    return np.array([[x[c] for c in FEATURES]])


def predict_patient(data):
    X = build_input(data)
    severity = float(model.predict(X)[0])

   
    MAX_SEVERITY = 40
    severity_normalized = (severity / MAX_SEVERITY) * 100

    disease = data["medical_condition"]
    admission = data["admission_type"]

    # ============================
    # Base initiale selon sévérité
    # ============================
    if severity_normalized < 35:  # Faible
        category = "🟢 Faible"
        base_doc, base_inf = 1, 1
        equip = {"monitor": 0, "pump": 0, "icu_bed": 0, "oxygen": 0}

    elif severity_normalized < 65:  # Moyenne
        category = "🟡 Moyenne"
        base_doc, base_inf = 2, 2
        equip = {"monitor": 1, "pump": 1, "icu_bed": 0, "oxygen": 1}

    else:  # Critique
        category = "🔴 Critique"
        base_doc, base_inf = 3, 3
        equip = {"monitor": 2, "pump": 2, "icu_bed": 1, "oxygen": 2}

    # =======================================
    # 🔍 AJUSTEMENTS SELON LA MALADIE
    # =======================================
    if disease == "Asthma":
        # Pas besoin d'ICU, surtout oxygène
        equip["oxygen"] += 1
        equip["monitor"] = 1  # Surveillance respiratoire

    elif disease == "Diabetes":
        equip["monitor"] = max(equip["monitor"], 1)
        equip["pump"] = 1   # perfusion parfois

    elif disease == "Cancer":
        equip["pump"] = max(equip["pump"], 2)      # chimio
        equip["icu_bed"] = max(equip["icu_bed"], 2) # cas sérieux
        equip["monitor"] = max(equip["monitor"], 1)
        equip["oxygen"] = max(equip["oxygen"], 1)
        base_doc, base_inf = 3, 3

    elif disease == "Trauma":
        equip["monitor"] = max(equip["monitor"], 1)
        equip["icu_bed"] = max(equip["icu_bed"], 1)

    elif disease == "Obesity":
        equip["monitor"] = 1
        equip["oxygen"] += 1

    elif disease == "Hypertension":
        equip["monitor"] = 1

    elif disease == "Arthritis":
        # Aucun besoin en ICU
        pass

    # =======================================
    # 🆘 Ajustement selon Admission Type
    # =======================================
    if admission == "Emergency":
        equip["monitor"] += 1
        equip["icu_bed"] += 1
        base_doc += 2
        base_inf += 2

    # =======================================
    # Résultat final
    # =======================================
    return severity_normalized, category, base_doc, base_inf, equip


