function fairePrediction() {
  const nom = document.getElementById("nom").value;
  const urgence = parseInt(document.getElementById("urgence").value);
  const specialite = document.getElementById("specialite").value;
  const distance = parseFloat(document.getElementById("distance").value);

  let resultat = "";

  if (urgence < 2) {
    resultat = "Recommandation : Télémédecine";
  } else {
    const hopital = choisirHopital(specialite, distance);
    resultat = "Hospitalisation recommandée à : " + hopital;
  }

  document.getElementById("resultat").innerText = resultat;
}

function choisirHopital(specialite, distance) {
  // Choisir un hôpital selon la spécialité
  const hopitaux = {
    "Cardiologie": "Hôpital Rotthalmünster",
    "Gériatrie": "Hôpital Vilshofen",
    "Radiologie": "Hôpital Wegscheid"
    // Ajouter d'autres spécialités ici
  };

  return hopitaux[specialite] || "Hôpital par défaut";
}
