# Générateur de Templates avec Gemini AI

Système automatisé qui scrape un site existant et génère un nouveau site web créatif avec Gemini AI.

## 🎯 Concept

**Input:**
- URL d'un site à scraper
- Thème du template (ex: "thérapeute", "coach", "yoga")

**Process:**
1. Scrape le site (textes, images, logo, contacts)
2. Envoie les données à Gemini Pro
3. Gemini génère un site créatif moderne

**Output:**
- Site HTML/CSS/JS complet
- Prêt pour validation manuelle

---

## 🎨 Comment ça marche

### Préservation de la structure

**Le principe clé :** "Même squelette, nouveau visuel"

Le système extrait et **préserve EXACTEMENT** la structure du site original :
- ✅ **Même ordre** des sections
- ✅ **Mêmes titres** (texte identique)
- ✅ **Mêmes paragraphes** (texte identique)
- ✅ **Mêmes listes** (contenu identique)
- ✅ **Vraies images** (URLs originales)
- ✅ **Informations de contact** (téléphone, email, logo)

**Ce qui change :** UNIQUEMENT le design visuel
- Palette de couleurs moderne
- Typographie professionnelle
- Layout contemporain
- Animations fluides
- Responsive design

**Résultat :** Le client dit *"C'est mon site mais en mieux !"*

### Extraction complète

Le scraper analyse le site et extrait :
```
Structure:
  Section 1: "À propos"
    - H2: "Mon parcours"
    - Paragraphe: "Texte complet..."
    - Paragraphe: "Suite..."
  Section 2: "Services"
    - H2: "Mes services"
    - Liste: [Service 1, Service 2, ...]
    - Paragraphe: "Description..."
  etc.
```

Gemini recrée cette structure **à l'identique** avec un design moderne.

---

## 📦 Installation

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Configurer la clé API Gemini

Obtenir une clé API: https://makersuite.google.com/app/apikey

**Option A: Variable d'environnement (recommandé)**
```bash
export GEMINI_API_KEY="votre_clé_api_ici"
```

**Option B: Fichier .env**
```bash
echo "GEMINI_API_KEY=votre_clé_api_ici" >> .env
```

**Option C: Passer en argument**
```bash
--api-key "votre_clé_api_ici"
```

---

## 🚀 Utilisation

### Exemple basique

```bash
python -m scripts.gemini_template_generator \
  --url "https://exemple-therapeute.com" \
  --theme "thérapeute"
```

### Avec prévisualisation automatique

```bash
python -m scripts.gemini_template_generator \
  --url "https://exemple-therapeute.com" \
  --theme "thérapeute" \
  --preview
```

### Avec clé API en argument

```bash
python -m scripts.gemini_template_generator \
  --url "https://exemple-coach.com" \
  --theme "coach sportif" \
  --api-key "AIza..."
```

---

## 📂 Structure de sortie

### Fichiers temporaires de scraping

Pendant le scraping, les fichiers temporaires sont stockés dans:
```
temp_files/gemini_therapeute/
├── screenshot_original.png    # Capture d'écran du site original
└── scraped_data.json          # Données brutes extraites
```

**Utilisation:**
- Créés automatiquement pendant le scraping
- Utilisés pour l'analyse et le débogage
- Peuvent être supprimés après génération réussie
- Ne sont PAS inclus dans le template final

### Fichiers générés (sortie finale)

Les templates générés sont stockés dans:
```
outputs/gemini_templates/gemini_therapeute/
├── index.html              # Site complet (HTML/CSS/JS)
├── scraped_data.json       # Données extraites du site source
└── README.md               # Guide de validation
```

**Description:**
- **index.html** - Template complet prêt pour déploiement (HTML/CSS/JS inline)
- **scraped_data.json** - Données extraites pour référence (structure, images URLs, contacts)
- **README.md** - Guide de validation manuelle avec checklist

**Dossier de sortie:** `outputs/gemini_templates/gemini_{theme}/`
- Où `{theme}` est le thème en minuscules avec underscores (ex: "coach sportif" → `gemini_coach_sportif`)

---

## 💰 Coûts Gemini

### Gemini 1.5 Pro (utilisé actuellement)
- **Input:** ~3-5k tokens par génération
- **Output:** ~5-8k tokens (site HTML complet)
- **Coût par site:** ~$0.03-0.05

### Optimisation des coûts

Pour utiliser **Gemini Flash** (10x moins cher):
```python
# Dans gemini_template_generator.py, ligne 39:
self.model = genai.GenerativeModel('gemini-1.5-flash')
```

**Coût avec Flash:** ~$0.002-0.003 par site

### Estimation pour volume

| Nombre de sites | Gemini Pro | Gemini Flash |
|----------------|------------|--------------|
| 10 sites       | $0.30-0.50 | $0.02-0.03   |
| 100 sites      | $3-5       | $0.20-0.30   |
| 1000 sites     | $30-50     | $2-3         |

---

## 🎨 Thèmes supportés

Exemples de thèmes efficaces:
- `"thérapeute"`
- `"coach sportif"`
- `"yoga"`
- `"psychologue"`
- `"ostéopathe"`
- `"nutritionniste"`
- `"photographe"`
- `"consultant"`

**Tip:** Plus le thème est spécifique, meilleur sera le design généré.

---

## ✅ Validation manuelle

### Checklist de validation

Après génération, vérifier:

1. **Design & Visuel**
   - [ ] Palette de couleurs professionnelle
   - [ ] Layout moderne et aéré
   - [ ] Typographie élégante
   - [ ] Animations fluides

2. **Contenu**
   - [ ] Tous les textes du site source sont présents
   - [ ] Informations de contact correctes (téléphone, email)
   - [ ] Sections cohérentes et bien organisées
   - [ ] Pas d'erreurs de français

3. **Responsive**
   - [ ] Fonctionne sur mobile
   - [ ] Fonctionne sur tablette
   - [ ] Navigation smooth

4. **Technique**
   - [ ] Formulaire de contact fonctionnel
   - [ ] Pas d'erreurs JavaScript
   - [ ] Images chargent correctement
   - [ ] Performance acceptable

### Ouvrir pour validation

```bash
# Linux/Mac
open outputs/gemini_templates/gemini_therapeute/index.html

# Ou directement dans le navigateur
firefox outputs/gemini_templates/gemini_therapeute/index.html
```

---

## 🔄 Workflow recommandé

### 1. Génération initiale

```bash
python -m scripts.gemini_template_generator \
  --url "https://site-source.com" \
  --theme "thérapeute" \
  --preview
```

### 2. Validation

Ouvrir `index.html` et vérifier la checklist ci-dessus.

### 3. Si ajustements nécessaires

**Option A: Régénérer avec Gemini**
```bash
# Même commande = nouvelle génération
python -m scripts.gemini_template_generator \
  --url "https://site-source.com" \
  --theme "thérapeute"
```

**Option B: Édition manuelle**
```bash
# Éditer directement le HTML
code outputs/gemini_templates/gemini_therapeute/index.html
```

### 4. Déploiement

Une fois validé:
- Copier `index.html` vers le serveur
- Ou utiliser un hosting gratuit (Netlify, Vercel, GitHub Pages)

---

## 🛠️ Personnalisation avancée

### Modifier le prompt Gemini

Éditer `scripts/gemini_template_generator.py`, méthode `_build_creative_prompt()`:

```python
def _build_creative_prompt(self, scraped_data):
    prompt = f"""
    Tu es un designer web créatif...

    [MODIFIER ICI pour changer le style de génération]
    """
    return prompt
```

### Utiliser Gemini Flash

```python
# Ligne 39
self.model = genai.GenerativeModel('gemini-1.5-flash')
```

### Ajouter des images custom

Le scraper télécharge automatiquement les images du site source dans:
```
temp_files/gemini_xxx/
├── logo.png
├── image_1.jpg
├── image_2.jpg
└── ...
```

Modifier le prompt pour référencer ces images.

---

## 🐛 Troubleshooting

### Test de connexion Gemini

Avant de générer des templates, testez votre connexion:

```bash
python -m scripts.test_gemini_connection
```

Ce script diagnostique automatiquement les problèmes de:
- Clé API
- Configuration proxy
- Connexion réseau
- Certificats SSL

### Erreur: "Clé API Gemini manquante"

```bash
export GEMINI_API_KEY="votre_clé"
# Ou ajouter au .env
```

### Erreur: "Timeout" ou "503 failed to connect"

**Cause:** Proxy d'entreprise ou firewall bloquant l'API Gemini

**Solution 1: Configurer le proxy**
```bash
# Linux/Mac
export HTTP_PROXY=http://proxy.entreprise.com:8080
export HTTPS_PROXY=http://proxy.entreprise.com:8080

# Windows PowerShell
$env:HTTP_PROXY="http://proxy.entreprise.com:8080"
$env:HTTPS_PROXY="http://proxy.entreprise.com:8080"

# Puis relancer
python -m scripts.gemini_template_generator --url URL --theme THEME
```

**Solution 2: Tester depuis un autre réseau**
- Essayer depuis un réseau sans proxy (téléphone 4G, réseau domestique)
- Si ça fonctionne, c'est un problème de proxy d'entreprise

**Solution 3: Vérifier le firewall**
L'API Gemini nécessite l'accès à:
- `generativelanguage.googleapis.com`
- Port 443 (HTTPS)

**Note:** Le système fait **3 tentatives automatiques** avec 5 secondes d'attente entre chaque.

### Erreur de scraping (site protégé)

Certains sites bloquent les scrapers. Solutions:
- Utiliser un proxy (configurer dans `config.py`)
- Désactiver SSL verification (déjà fait par défaut)

### Génération trop lente

Utiliser Gemini Flash au lieu de Pro:
```python
self.model = genai.GenerativeModel('gemini-1.5-flash')
```

### Design pas assez créatif

- Être plus spécifique dans le thème: `"thérapeute holistique nature"` au lieu de `"thérapeute"`
- Modifier le prompt pour insister sur certains aspects
- Régénérer plusieurs fois et choisir la meilleure

---

## 📊 Utilisation en batch

### Générer plusieurs templates

```bash
#!/bin/bash

# Liste de sites à transformer
urls=(
  "https://site1.com|thérapeute"
  "https://site2.com|coach"
  "https://site3.com|yoga"
)

for entry in "${urls[@]}"; do
  IFS='|' read -r url theme <<< "$entry"

  echo "Génération: $theme - $url"

  python -m scripts.gemini_template_generator \
    --url "$url" \
    --theme "$theme"

  sleep 2  # Éviter rate limiting
done
```

---

## 🎯 Prochaines améliorations possibles

- [ ] Support multi-pages (pas seulement one-page)
- [ ] Génération d'images avec Imagen
- [ ] A/B testing automatique (générer 2-3 variants)
- [ ] Analyse de performance (Lighthouse scores)
- [ ] Export vers CMS (WordPress, Webflow)
- [ ] Génération de variantes de couleurs
- [ ] Support de templates personnalisés

---

## 💡 Exemples de résultats

### Avant → Après

**Site source:** Site WordPress basique de thérapeute avec 5 sections

**Structure préservée:**
```
1. Accueil - "Bienvenue" + paragraphe de présentation
2. À propos - "Mon parcours" + 3 paragraphes
3. Services - "Mes prestations" + liste de 5 services + description
4. Témoignages - 3 citations de clients
5. Contact - Formulaire + coordonnées
```

**Généré:** Site moderne one-page avec:
- ✅ **MÊMES 5 sections** dans le même ordre
- ✅ **MÊMES textes** (aucun changement de contenu)
- ✅ **MÊMES images** du site original
- 🎨 Palette de couleurs apaisante (thérapeute)
- 🎨 Typographie élégante (Playfair Display + Raleway)
- 🎨 Hero section avec dégradé subtil
- 🎨 Cards avec ombres douces
- 🎨 Animations smooth au scroll
- 🎨 Design épuré et professionnel

**Résultat:** Le client reconnaît immédiatement son contenu, mais le trouve magnifique.

**Temps de génération:** ~30-60 secondes
**Coût:** $0.03-0.05

### Exemple concret

**Avant (site original):**
```html
<div>
  <h2>Mes services</h2>
  <p>Je propose des séances individuelles...</p>
  <ul>
    <li>Thérapie cognitive</li>
    <li>Hypnose</li>
  </ul>
</div>
```

**Après (site généré):**
```html
<section class="services">
  <h2>Mes services</h2>
  <p>Je propose des séances individuelles...</p>
  <ul class="service-list">
    <li>Thérapie cognitive</li>
    <li>Hypnose</li>
  </ul>
</section>
```
**Mêmes textes, design moderne avec classes CSS professionnelles**

---

## 📞 Support

Pour des questions ou problèmes:
1. Vérifier la section Troubleshooting ci-dessus
2. Vérifier les logs dans la console
3. Tester avec un site simple d'abord

---

**Happy generating! 🚀**
