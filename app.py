import streamlit as st
import streamlit.components.v1 as components
from groq import Groq

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="AdGenius Pro", page_icon="📣", layout="wide")

# Design pro et suppression de la sidebar
st.markdown("""
<style>
[data-testid="stSidebar"] {display: none !important;}
[data-testid="stSidebarNav"] {display: none !important;}
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# CONFIGURATION PAYPAL
# -------------------------
PAYPAL_CLIENT_ID = "DEMO"  
PAYPAL_PLAN_ID = "DEMO"    

# -------------------------
# GESTION DE L'ACCÈS
# -------------------------
if "est_abonne" not in st.session_state:
    st.session_state.est_abonne = False

try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except:
    API_KEY = ""

# -------------------------
# INTERFACE SÉCURISÉE
# -------------------------
st.title("📣 AdGenius Pro")
st.subheader("Générez des textes publicitaires Facebook & Instagram à fort taux de clic en 2 secondes.")

# CAS 1 : L'UTILISATEUR N'A PAS PAYÉ
if not st.session_state.est_abonne:
    st.warning("🔒 Cette application est réservée aux membres de la version Premium.")
    col_offre, col_connexion = st.columns(2, gap="large")
    
    with col_offre:
        st.subheader("🚀 Explosez vos ventes pour 30 $/mois")
        st.write("Arrêtez de brûler votre budget publicitaire. Obtenez des textes accrocheurs basés sur les meilleurs frameworks de copywriting du monde (AIDA, PAS).")
        st.write("Le paiement est entièrement sécurisé par **PayPal**.")
        
        if PAYPAL_CLIENT_ID == "DEMO":
            paypal_html = """
            <a href="https://paypal.com" target="_blank" style="text-decoration: none;">
                <div style="background-color: #ffc439; color: #003087; text-align: center; 
                            padding: 12px; font-family: Arial, sans-serif; font-weight: bold; 
                            border-radius: 4px; max-width: 300px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🟨 S'abonner avec PayPal (Démo)
                </div>
            </a>
            """
        else:
            paypal_html = f"""
            <div id="paypal-button-container-fixed" style="max-width: 350px; margin-top: 20px;"></div>
            <script src="https://paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID}&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
            <script>
              paypal.Buttons({{
                  style: {{ shape: 'rect', color: 'gold', layout: 'vertical', label: 'subscribe' }},
                  createSubscription: function(data, actions) {{ return actions.subscription.create({{ 'plan_id': '{PAYPAL_PLAN_ID}' }}); }},
                  onApprove: function(data, actions) {{ alert('Abonnement réussi ! ID : ' + data.subscriptionID); }}
              }}).render('#paypal-button-container-fixed');
            </script>
            """
        components.html(paypal_html, height=150, scrolling=False)
        
    with col_connexion:
        st.subheader("🔑 Déjà abonné ?")
        email = st.text_input("Adresse e-mail")
        mot_de_passe = st.text_input("Mot de passe", type="password")
        
        if st.button("Se connecter", use_container_width=True):
            if email == "test@client.com" and mot_de_passe == "ads30":
                st.session_state.est_abonne = True
                st.success("Accès accordé !")
                st.rerun()
            else:
                st.error("Identifiants incorrects.")

# CAS 2 : L'UTILISATEUR EST ABONNÉ
else:
    st.write("✨ **Espace Publicitaire Actif.** Maximisez votre ROI.")
    if st.button("🚪 Se déconnecter", key="logout"):
        st.session_state.est_abonne = False
        st.rerun()
        
    st.write("---")

    with st.container(border=True):
        col_inputs, col_options = st.columns(2)
        
        with col_inputs:
            produit = st.text_input("Nom du produit ou service :", placeholder="Ex: Gourde auto-nettoyante UV, Formation Crypto")
            description = st.text_area("Bénéfices principaux / Offre :", placeholder="Ex: Élimine 99% des bactéries, garde l'eau fraîche 24h. Réduction de -20% ce week-end.")
            
        with col_options:
            framework = st.selectbox("Framework de Copywriting", [
                "🔥 AIDA (Attention, Intérêt, Désir, Action)",
                "⚠️ PAS (Problème, Agitation, Solution)",
                "⚡ Hook-Story-Offer (Accroche, Histoire courte, Offre)"
            ])
            audience = st.text_input("Audience cible :", placeholder="Ex: Sportifs, Randonneurs, Jeunes actifs")

        generer = st.button("🚀 Générer mes Publicités", use_container_width=True)

    if generer:
        if not API_KEY:
            st.error("⚠️ Clé GROQ_API_KEY manquante.")
        elif not produit or not description:
            st.error("⚠️ Remplissez le nom du produit et la description.")
        else:
            with st.spinner("Groq crée vos variantes publicitaires..."):
                try:
                    client = Groq(api_key=API_KEY)
                    
                    prompt_systeme = """Tu es un media buyer d'élite et un copywriter publicitaire de génie spécialisé en Facebook Ads et Instagram Ads.
                    Ton but est de rédiger 3 variantes de textes publicitaires percutants basés sur le framework demandé.
                    Inclus des accroches fortes (hooks), des émojis adaptés, des listes à puces pour les bénéfices, et un Appel à l'Action (CTA) clair.
                    Ne fais aucune intro ou conclusion amicale, donne directement les 3 variantes."""

                    prompt_utilisateur = f"Produit: {produit}\nBénéfices: {description}\nFramework: {framework}\nCible: {audience}"

                    reponse = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": prompt_systeme},
                            {"role": "user", "content": prompt_utilisateur}
                        ],
                        temperature=0.7
                    )
                    
                    ads_genere = reponse.choices[0].message.content
                    st.success("✨ Vos variantes publicitaires sont prêtes !")
                    st.markdown(ads_genere)
                    st.text_area("Copier les textes :", value=ads_genere, height=300)

                except Exception as e:
                    st.error(f"Erreur technique Groq : {str(e)}")
