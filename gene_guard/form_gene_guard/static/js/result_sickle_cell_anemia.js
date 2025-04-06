

//pour recuperer les donneees est faire le traitement
function fetchAndProcessData() {
    let dataDict = {};  // Créer un dictionnaire vide pour stocker les données

    fetch('/get-sickle-cell-results/')  // URL définie dans urls.py
        .then(response => response.json())
        .then(data => {
            console.log(data);  // Affiche les données récupérées
            // On peut maintenant les affecter au dictionnaire
            dataDict = { ...data }; 
            console.log(dataDict); // Assigner les données à dataDict
            const taille = Object.keys(dataDict).length;
            console.log(taille);
            
           
            

            // Traite les données dans dataDict
            processData(dataDict);  // Exemple de traitement des données
            const risk = processData(dataDict);  // Exemple de traitement des données
            console.log(`Risque calculé : ${risk}%`);
        })
        .catch(error => console.error("Erreur:", error));
}

function processData(dataDict) {
    let risk = 0;
    let risk1=0;

    // 1. Facteurs génétiques
    if (dataDict.bothparents === "yes") {
        risk += 35; // 25% de risque si les deux parents sont porteurs
    }
    if (dataDict.familyHistory === "yes") {
        risk += 10; // Antécédents familiaux augmentent le risque
    }

    // 2. Résultats de test (prioritaires sur tout le reste)
    if (dataDict.testResult) {
        switch(dataDict.testResult) {
            case "HbSS":
                return 81; // Diagnostic confirmé
            case "HbAS":
                risk += 10; // Porteur sain
                break;
            case "HbA":
                risk+=0; // Normal
            default:
                // Pour d'autres résultats comme HbSC, HbSβ-thalassémie
                risk += 20;
        }
    }

    // 3. Si un test drépanocytose a été fait
    if (dataDict.sickle === "yes" && !dataDict.testResult) {
        risk = 100; // Considéré comme positif si pas de résultat détaillé
    }

    // 4. Symptômes cliniques
    const symptoms = [
        "FrequentPain",
        "abdominalPain",
        "yellow",
        "bloodTransfusion"
    ];
    
    let symptomCount = 0;
    symptoms.forEach(symptom => {
        if (dataDict[symptom] === "yes") {
            symptomCount++;
        }
    });

    // Ajout du risque basé sur les symptômes
    if (symptomCount > 0) {
        risk += symptomCount * 8;
    }

    // 5. Facteurs ethniques
    const highRiskGroups = ["Africain", "Méditerranéen", "Antillais"];
    if (highRiskGroups.includes(dataDict.ethnicGroup)) {
        risk += 10;
    }

    // 6. Autres facteurs
    if (dataDict.history === "yes") {
        risk += 15; // Antécédents médicaux liés
    }
    if (dataDict.diet === "yes") {
        risk += 5; // Régime spécifique suggère une prise en charge
    }
    if (dataDict.smoking === "yes") {
        risk += 5; // Aggravation des symptômes
    }

    // 7. Si déjà diagnostiqué
    if (dataDict.diagnosed === "yes") {
        return 78;
    }

    
    return risk;
}


fetchAndProcessData();

document.getElementById("risk-result").innerText = processData(dataDict) ;

 

