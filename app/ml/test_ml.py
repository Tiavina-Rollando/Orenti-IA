from data.models import UserProfile
from ml.recommender import generate_recommendations

profile = UserProfile(
    niveau="Terminale",
    matieres_preferees=["Mathématiques", "Informatique"],
    # Utilisation des identifiants exacts des colonnes de matières du dataset
    resultats_scolaires={
        "mathematiques": 16.0,
        "informatique": 17.0,
        "physique": 14.0,
    },
    competences=["Python", "Programmation"],
    centres_interet=["Intelligence artificielle", "Data Science"],
    activites_projets=["Création d'une application Python"],
    preferences_professionnelles=["Développeur logiciel", "Data Scientist"],
    environnement_travail=["Travail en équipe", "Bureau"],
)

result = generate_recommendations(profile, top_k=3)

for recommendation in result.recommendations:
    print(recommendation.parcours, "=>", recommendation.score)