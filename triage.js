document.getElementById("predictionForm").addEventListener("submit", function(event) {
  event.preventDefault();

  // 🔽 Données du formulaire
  const patient = {
    Lastname: document.getElementById("lastname").value.trim(),
    Firstname: document.getElementById("firstname").value.trim(),
    Age: parseInt(document.getElementById("age").value),
    Urgency: parseInt(document.getElementById("urgency").value),
    Specialty: document.getElementById("specialty").value,
    Distance: parseInt(document.getElementById("distance").value),
    Availability: parseInt(document.getElementById("availability").value),
    Date: new Date().toISOString().slice(0, 10)
  };

  // 🔍 Logique de prédiction IA basée sur ton document
  let recommendation = "No recommendation available";
  let hospital = "Télémédecine only";

  // Cas généraux
  if (patient.Urgency === 0 && patient.Age >= 10 && patient.Age <= 80) {
    recommendation = "Telemedicine (non-urgent)";
  } else {
    switch (patient.Specialty) {
      case "Dermatology":
        recommendation = (patient.Urgency === 0 && patient.Age >= 10 && patient.Age <= 80)
          ? "Telemedicine"
          : "Hospital referral";
        break;

      case "Cardiology":
        recommendation = (patient.Urgency >= 1)
          ? "Hospital referral"
          : "Telemedicine likely sufficient";
        break;

      case "Pediatrics":
        recommendation = (patient.Age < 5)
          ? "Emergency hospital referral (child under 5)"
          : "Telemedicine";
        break;

      case "Geriatrics":
        recommendation = (patient.Age > 80 || patient.Urgency >= 1)
          ? "Hospital referral (elderly case)"
          : "Telemedicine";
        break;

      case "Stroke":
      case "Neurosurgery":
        recommendation = "Immediate hospital referral (neurological emergency)";
        break;

      case "Radiology":
        recommendation = "Physical presence required → hospital referral";
        break;

      case "Pulmonology":
        recommendation = (patient.Age < 5 || patient.Age > 80 || patient.Urgency === 2)
          ? "Hospital referral"
          : "Telemedicine for mild symptoms";
        break;

      case "Psychosomatic":
        recommendation = "Telemedicine if stable and autonomous";
        break;

      default:
        recommendation = (patient.Urgency >= 1)
          ? "Hospital referral"
          : "Telemedicine possible";
    }
  }

  // 📢 Affichage
  document.getElementById("recommendation").innerText = `Recommendation: ${recommendation}`;
});
