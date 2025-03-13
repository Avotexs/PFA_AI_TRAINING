from django.shortcuts import render, HttpResponse , redirect

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


def resultat(request):
    return render(request,'welcome/resultat.html',{'title':'Resultat'})