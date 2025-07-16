let currentPatient = null; // Temp data before confirmation

// 1. Quand on soumet le formulaire, on fait juste une recommandation
document.getElementById("predictionForm").addEventListener("submit", function(event) {
  event.preventDefault();

  // Récupérer les valeurs du formulaire
  const lastname = document.getElementById("lastname").value.trim();
  const firstname = document.getElementById("firstname").value.trim();
  const age = parseInt(document.getElementById("age").value);
  const urgency = parseInt(document.getElementById("urgency").value);
  const specialty = document.getElementById("specialty").value;
  const distance = parseInt(document.getElementById("distance").value);
  const availability = parseInt(document.getElementById("availability").value);
  const today = new Date().toISOString().slice(0, 10);

  // Préparer l'objet patient
  currentPatient = {
    Nom: lastname,
    Prénom: firstname,
    Age: age,
    Urgence: urgency,
    Specialite: specialty,
    Distance: distance,
    Disponibilite: availability,
    Date: today
  };

  // 2. Logique IA : recommandations personnalisées
  let reco = "No recommendation available";

  if (urgency === 0 && age >= 10 && age <= 80) {
    reco = "Telemedicine (non-urgent case)";
  } else {
    switch (specialty) {
      case "Dermatology":
        reco = (urgency === 0 && age >= 10 && age <= 80)
          ? "Telemedicine"
          : "Hospital referral";
        break;

      case "Cardiology":
        reco = urgency >= 1 ? "Hospital referral" : "Telemedicine likely sufficient";
        break;

      case "Pediatrics":
        reco = age < 5 ? "Emergency hospital referral (child under 5)" : "Telemedicine";
        break;

      case "Geriatrics":
        reco = age > 80 || urgency >= 1 ? "Hospital referral (elderly case)" : "Telemedicine";
        break;

      case "Stroke":
      case "Neurosurgery":
        reco = "Immediate hospital referral (neurological emergency)";
        break;

      case "Radiology":
        reco = "Hospital referral (exam requires presence)";
        break;

      case "Pulmonology":
        reco = (age < 5 || age > 80 || urgency === 2)
          ? "Hospital referral"
          : "Telemedicine for mild respiratory symptoms";
        break;

      case "Psychosomatic":
        reco = "Telemedicine if stable and autonomous";
        break;

      default:
        reco = urgency >= 1 ? "Hospital referral" : "Telemedicine possible";
    }
  }

  // Ajouter la recommandation à l'objet
  currentPatient.Recommandation = reco;

  // 3. Afficher la recommandation à l'écran
  document.getElementById("recommendation").innerText = `🧠 Recommendation: ${reco}`;
  document.getElementById("confirmBtn").style.display = "inline-block";
});

// 4. Si on clique sur le bouton de confirmation => POST vers /add_patient
document.getElementById("confirmBtn").addEventListener("click", function () {
  if (!currentPatient) {
    alert("No patient data to confirm.");
    return;
  }

  fetch("/add_patient", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(currentPatient)
  })
    .then(response => response.json())
    .then(data => {
      alert("✅ Patient successfully admitted!");
      window.location.href = "admissions.html";
    })
    .catch(error => {
      console.error("Error:", error);
      alert("❌ Error saving patient.");
    });
});
