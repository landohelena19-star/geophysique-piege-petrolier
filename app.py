import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Géophysique Pétrolière - Gravimétrie", layout="wide")

st.title("🛢️ Exploration Pétrolière : Détection d'un Piège par Gravimétrie")
st.markdown("""
Cette application simule la réponse gravimétrique de surface au-dessus d'une structure géologique 
typique de l'exploration pétrolière : un **dôme de sel** (qui agit souvent comme piège à hydrocarbures).
Le sel ayant une densité plus faible que les sédiments encaissants, il crée une anomalie négative de gravité.
""")
# Barre latérale : Paramètres interactifs
st.sidebar.header("Paramètres du Réservoir / Dôme")

depth = st.sidebar.slider("Profondeur du centre (m)", min_value=200, max_value=3000, value=1000, step=100)
radius = st.sidebar.slider("Rayon de la structure (m)", min_value=100, max_value=1500, value=500, step=50)
delta_rho = st.sidebar.slider(
    "Contraste de densité Δρ (g/cm³)", 
    min_value=-0.6, 
    max_value=0.6, 
    value=-0.3, 
    step=0.05,
    help="Négatif pour un dôme de sel, positif pour une intrusion dense."
)
# Constante de gravitation (SI)
G = 6.67430e-11  # m³ / (kg · s²)

# Conversion du contraste de densité en kg/m³
delta_rho_kg = delta_rho * 1000

# Volume et masse en excès / déficit
volume = (4.0 / 3.0) * np.pi * (radius ** 3)
delta_mass = delta_rho_kg * volume

# Profil de mesure en surface (le long d'une ligne de -5000 m à +5000 m)
x = np.linspace(-5000, 5000, 500)

# Formule analytique de l'attraction gravimétrique verticale (anomalie gz en mGal)
gz_ms2 = G * delta_mass * depth / ((x ** 2 + depth ** 2) ** (1.5))
gz_mgal = gz_ms2 * 1e5  # 1 m/s² = 10^5 mGal

# Affichage des métriques clés
col1, col2, col3 = st.columns(3)
col1.metric("Masse anomale estimée", f"{delta_mass / 1e9:.2f} Mt")
col2.metric("Anomalie maximale", f"{np.max(np.abs(gz_mgal)):.2f} mGal")
col3.metric("Type d'anomalie", "Déficit gravimétrique" if delta_rho < 0 else "Excès gravimétrique")

# Tracé des graphiques
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, gridspec_kw={'height_ratios': [1, 1.2]})

# 1. Profil gravimétrique
ax1.plot(x / 1000, gz_mgal, color="crimson", lw=2.5, label="Anomalie $\Delta g_z$ mesurée")
ax1.axhline(0, color="gray", linestyle="--", alpha=0.7)
ax1.set_ylabel("Gravité résiduelle (mGal)", fontsize=11)
ax1.set_title("Mesure gravimétrique en surface (Profil)", fontsize=13, fontweight="bold")
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(loc="upper right")

# 2. Coupe géologique du sous-sol
ax2.set_facecolor("#e8d8c8")  # Sédiments encaissants
circle = plt.Circle((0, depth), radius, color="#f5f5f5" if delta_rho < 0 else "#666666", ec="black", lw=2, label="Dôme de sel / Réservoir")
ax2.add_patch(circle)

# Inversion de l'axe Y pour représenter la profondeur vers le bas
ax2.set_ylim(3500, 0)
ax2.set_xlim(-5, 5)
ax2.set_xlabel("Distance le long du profil (km)", fontsize=11)
ax2.set_ylabel("Profondeur (m)", fontsize=11)
ax2.set_title("Modèle géologique 2D", fontsize=13, fontweight="bold")
ax2.axhline(0, color="green", lw=3, label="Surface du sol")
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(loc="lower right")

st.pyplot(fig)

# Explications géophysiques pour la présentation
st.subheader("Interprétation géophysique pour l'évaluation")
st.write("""
* **Effet de la profondeur :** Plus le réservoir est profond, plus l'anomalie est étalée et de faible amplitude.
* **Effet de la taille :** Le volume augmente proportionnellement au cube du rayon ($R^3$), amplifiant très fortement le signal.
* **Contexte pétrolier :** Les hydrocarbures migrent vers le haut et se retrouvent piégés contre les flancs imperméables du sel. Identifier cette signature gravimétrique négative permet de cibler les forages exploratoires.
""")
