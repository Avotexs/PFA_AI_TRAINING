from django.shortcuts import render, HttpResponse , redirect
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import joblib
import numpy as np
# Create your views here.
def home(request):
    
    return render(request,'welcome/home.html',{'title':'GeneGuard'})
    
def test_guidelines(request):
    return render(request,'welcome/test_guidelines.html',{'title':'GeneGuard'})

def test_finish(request):
    return render(request,'welcome/test_finish.html',{'title':'GeneGuard'})


def formulaire_Sickle_cell_anemia(request):
    return render(request,'welcome/Sickle_cell_anemia_form.html',{'title':'Formulaire'})

def formulaire_Galactosemia(request):
    return render(request,'welcome/Galactosemia_form.html',{'title':'Formulaire'})


def formulaire(request):
    return render(request,'welcome/formulaire.html',{'title':'Formulaire'})

def formulaire(request):
    return render(request,'welcome/hypercholesterolemia.html',{'title':'Formulaire'})

def resultat(request):
    return render(request,'welcome/resultat.html',{'title':'Resultat'})

def ListeMaladie(request):
    return render(request,'welcome/ListeMaladie.html',{'title':'ListeMaladie'})

def formulaire_diabetes(request):
    return render(request, 'welcome/resultat-diabetes.html', {'title': 'Évaluation Diabète'})
def resultat_diabete(request):
    result_raw = request.session.get('diabetes_result', '')
    parts = result_raw.split("Probabilité estimée : ")
    conseil = parts[0] if len(parts) > 0 else ""
    pourcentage_str = parts[1].replace(" %", "") if len(parts) > 1 else "0"
    
    try:
        pourcentage = float(pourcentage_str)
    except:
        pourcentage = 0

    return render(request, 'welcome/resultat_diabete.html', {
        'conseil': conseil.strip(),
        'pourcentage': pourcentage
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SickleCellResult  # Import du modèle

@csrf_exempt  # Désactive la protection CSRF (utile pour le développement)
def save_sickle_cell_result(request):
    if request.method == "POST":  # Vérifie si la requête est POST
        try:
            data = json.loads(request.body)  # Convertit le JSON reçu en dictionnaire Python
            result = SickleCellResult.objects.create(responses=data)  # Enregistre en base
            return JsonResponse({"message": "Données enregistrées avec succès", "id": result.user_id}, status=201)  
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)  # En cas d'erreur
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)  # Si ce n'est pas une requête POST





def get_sickle_cell_results(request):
    # Récupérer le dernier enregistrement
    result = SickleCellResult.objects.last()  # Récupère le dernier enregistrement
    
    if result:
        # Si un résultat existe, retourner les réponses sous forme de JSON
        return JsonResponse(result.responses, safe=False)
    else:
        # Si aucun résultat n'est trouvé, renvoyer une erreur
        return JsonResponse({"error": "Aucun résultat trouvé."}, status=404)

#model training
@csrf_exempt
def predict_diabetes_result(request):
    if request.method == 'POST':
        try:
            data = request.POST
            features = [
                float(data.get("Pregnancies")),
                float(data.get("Glucose")),
                float(data.get("BloodPressure")),
                float(data.get("SkinThickness")),
                float(data.get("Insulin")),
                float(data.get("BMI")),
                float(data.get("DiabetesPedigreeFunction")),
                float(data.get("Age")),
            ]
            model_path = os.path.join(os.path.dirname(__file__), 'ml_model', 'diabetes_model.pkl')
            model = joblib.load(model_path)

            probability = model.predict_proba([features])[0][1]
            percentage = round(probability * 100, 2)
            result_text = "⚠️ High risk of diabetes" if percentage >= 50 else "✅ Low risk of diabetes"
            full_result = f"{result_text} Probabilité estimée : {percentage} %"

            # Stocker le résultat dans la session
            request.session['diabetes_result'] = full_result
            return JsonResponse({"redirect_url": "/Resultat/diabete/"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
