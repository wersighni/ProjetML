import joblib
import numpy as np
from django.shortcuts import render

from .forms import PatientForm
from .ml_model import predict_patient

from django.shortcuts import render

def home(request):
    return render(request, "home.html")


def choose_count(request):
    if request.method == "POST":
        num = request.POST.get("num")
        if num and num.isdigit():
            n = int(num)
            return render(request, "multi_form.html", {
                "forms": [PatientForm(prefix=str(i)) for i in range(n)],
                "n": n
            })
    return render(request, "choose_count.html")


def multi_form(request, n):
    forms = [PatientForm(request.POST or None, prefix=str(i)) for i in range(n)]

    if request.method == "POST":
        if all(f.is_valid() for f in forms):
            results = []
            total_docs = total_inf = 0
            total_equipment = {"monitor": 0, "pump": 0, "icu_bed": 0, "oxygen": 0}

            for f in forms:
                data = f.cleaned_data
                severity, category, doc, inf, equip = predict_patient(data)

                results.append((severity, category, doc, inf, equip))

                total_docs += doc
                total_inf += inf

                for k in total_equipment:
                    total_equipment[k] += equip[k]

            return render(request, "multi_result.html", {
                "results": results,
                "total_docs": total_docs,
                "total_inf": total_inf,
                "total_equipment": total_equipment,
            })

    return render(request, "multi_form.html", {
        "forms": forms,
        "n": n
    })




# Charger le modèle + scaler + label encoder
model = joblib.load("predictor/model_files/model.pkl")
scaler = joblib.load("predictor/model_files/scaler.pkl")
encoder = joblib.load("predictor/model_files/label_encoder.pkl")

def predict_view(request):
    prediction = None

    if request.method == "POST":
        try:
            # 1️⃣ Lire les inputs
            data = [
                float(request.POST.get("glucose")),
                float(request.POST.get("creatinine")),
                float(request.POST.get("hemoglobine")),
                float(request.POST.get("leucocytes")),
                float(request.POST.get("alt")),
                float(request.POST.get("ast")),
                float(request.POST.get("age")),
                float(request.POST.get("temperature")),
                float(request.POST.get("pouls")),
                float(request.POST.get("pression_systolique")),
                int(request.POST.get("diabete")),
                int(request.POST.get("hypertension")),
                int(request.POST.get("tabagisme")),
            ]

            # 2️⃣ Transformer en array
            features = np.array([data])

            # 3️⃣ Appliquer le scaler comme pendant l'entraînement
            features_scaled = scaler.transform(features)

            # 4️⃣ Prédiction brute (0,1,2)
            pred_id = model.predict(features_scaled)[0]

            # 5️⃣ Convertir ID → label
            prediction = encoder.inverse_transform([pred_id])[0]

        except Exception as e:
            prediction = f"Erreur : {e}"

    return render(request, "form.html", {"prediction": prediction})
