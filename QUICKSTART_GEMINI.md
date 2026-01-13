# 🚀 Quick Start - Redesign de sites avec Gemini

**Transformez n'importe quel site en version moderne et esthétique**

## 🎯 Comment ça marche

**Input:** URL du site du client (ex: `https://site-client-actuel.com`)
**Output:** Le MÊME site redesigné avec un visuel moderne et professionnel

### Processus:

1. **Scrape** → Extrait TOUT le contenu du site existant
   - Tous les textes (identiques)
   - Toutes les images (mêmes URLs)
   - La structure exacte (même ordre)

2. **Gemini Redesign** → Génère le site avec un nouveau visuel
   - ✅ **Contenu identique** (textes du site original)
   - ✅ **Structure identique** (sections dans le même ordre)
   - ✅ **Images identiques** (URLs du site original)
   - 🎨 **Design moderne et esthétique** (nouveau visuel)

3. **Résultat** → Site redesigné prêt pour validation
   - Le client reconnaît son site
   - Mais avec un visuel professionnel et moderne

### Ce qui est préservé (contenu original):
- ✅ Tous les textes du site (identiques)
- ✅ Toutes les images (mêmes URLs)
- ✅ Structure et ordre des sections
- ✅ Logos et éléments de marque

### Ce qui change (nouveau design):
- 🎨 Palette de couleurs moderne
- 🎨 Typographie professionnelle
- 🎨 Layout contemporain et aéré
- 🎨 Animations et transitions fluides
- 🎨 Design responsive (mobile/desktop)

**Résultat:** Le client voit "C'est mon site, mais en magnifique !"

## Installation rapide

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer la clé API Gemini
export GEMINI_API_KEY="votre_clé_api"
# Obtenir une clé: https://makersuite.google.com/app/apikey

# 3. Tester la connexion (recommandé)
python -m scripts.test_gemini_connection
```

### Configuration proxy (si nécessaire)

Si vous êtes derrière un proxy d'entreprise:

```bash
# Linux/Mac
export HTTP_PROXY=http://proxy.entreprise.com:8080
export HTTPS_PROXY=http://proxy.entreprise.com:8080

# Windows PowerShell
$env:HTTP_PROXY="http://proxy.entreprise.com:8080"
$env:HTTPS_PROXY="http://proxy.entreprise.com:8080"
```

## Utilisation

### Redesigner un site (mode complet)

```bash
# Prendre le site du client et générer une version moderne
python -m scripts.gemini_template_generator \
  --url "https://site-du-client.com" \
  --theme "moderne et élégant"
```

**Le paramètre `--theme`:** Guide le style visuel du redesign
- `"moderne et élégant"` → Design épuré, contemporain
- `"chaleureux et accueillant"` → Couleurs douces, ambiance conviviale
- `"professionnel"` → Design corporate, sérieux
- `"dynamique"` → Couleurs vives, énergique

### Régénérer avec un style différent (mode rapide)

Si vous voulez tester plusieurs styles visuels sans rescraper:

```bash
# Utiliser les données déjà extraites du site client
python -m scripts.gemini_template_generator \
  --data-file "temp_files/gemini_moderne_et_elegant/scraped_data.json" \
  --theme "chaleureux et accueillant"
```

**Avantages:**
- ⚡ Plus rapide (skip le scraping)
- 🔄 Tester plusieurs styles visuels rapidement
- 💰 Économise les ressources
- 🎨 Trouver le meilleur design pour le client

### Avec prévisualisation automatique

```bash
# Ouvre automatiquement le site redesigné dans le navigateur
python -m scripts.gemini_template_generator \
  --url "https://site-du-client.com" \
  --theme "moderne et élégant" \
  --preview
```

## Résultat

Fichiers générés dans: `outputs/gemini_templates/gemini_moderne_et_elegant/`

```
gemini_therapeute/
├── index.html           # Site complet (HTML/CSS/JS)
├── scraped_data.json    # Données extraites
└── README.md            # Guide de validation
```

## 📂 Stockage des fichiers

### Fichiers temporaires (pendant le scraping)
```
temp_files/gemini_moderne_et_elegant/
├── screenshot_original.png    # Capture du site original du client
└── scraped_data.json          # Contenu extrait (textes, images, structure)
```
**Note:** Fichiers temporaires créés pendant le scraping, réutilisables pour tester d'autres styles.

### Fichiers générés (site redesigné final)
```
outputs/gemini_templates/gemini_moderne_et_elegant/
├── index.html           # Site redesigné complet (HTML/CSS/JS inline)
├── scraped_data.json    # Données du site original (pour référence)
└── README.md            # Checklist de validation
```
**Note:** Le dossier final contient le site redesigné prêt pour validation client.

## Workflow

### Mode complet (avec scraping)
1. **Input** → URL du site actuel du client
2. **Scraping** → Extraction de tout le contenu (textes, images, structure)
3. **Gemini Redesign** → Génération du site avec nouveau visuel
4. **Validation** → Le client vérifie et approuve
5. **Déploiement** → Mise en ligne du site redesigné

### Mode rapide (tester plusieurs styles)
1. **Scraping initial** → Fait une seule fois
2. **Gemini Redesign** → Génère avec style A (ex: "moderne")
3. **Gemini Redesign** → Génère avec style B (ex: "chaleureux")
4. **Gemini Redesign** → Génère avec style C (ex: "professionnel")
5. **Choix client** → Le client choisit son préféré
6. **Déploiement** → Mise en ligne de la version choisie

## Coûts par redesign

- **Gemini Pro** (recommandé): ~$0.03-0.05 par redesign
- **Gemini Flash** (rapide): ~$0.002-0.003 par redesign

**Exemple:**
- Redesigner 1 site avec 3 styles différents = ~$0.09-0.15 (Gemini Pro)
- Redesigner 100 sites = ~$0.20-0.30 (Gemini Flash)

## Documentation complète

Voir: [`docs/GEMINI_TEMPLATE_GENERATOR.md`](docs/GEMINI_TEMPLATE_GENERATOR.md)

## Exemples concrets

### Cas 1: Redesigner le site d'un thérapeute

```bash
# Le site actuel est vieux et pas esthétique
# Générer une version moderne avec le même contenu
python -m scripts.gemini_template_generator \
  --url "https://cabinet-therapie-dupont.fr" \
  --theme "apaisant et professionnel" \
  --preview
```

**Résultat:** Même contenu (textes, offres, photos) mais design moderne et esthétique

### Cas 2: Redesigner le site d'un restaurant

```bash
# Le site du restaurant est basique
# Générer une version appétissante et moderne
python -m scripts.gemini_template_generator \
  --url "https://restaurant-labelleassiette.fr" \
  --theme "gastronomique et élégant" \
  --preview
```

**Résultat:** Menu identique, photos identiques, mais design qui donne faim !

### Cas 3: Tester plusieurs styles pour le même client

```bash
# 1. Scraper le site une seule fois
python -m scripts.gemini_template_generator \
  --url "https://yoga-studio-paris.fr" \
  --theme "zen et minimaliste"

# 2. Tester d'autres styles sans rescraper
python -m scripts.gemini_template_generator \
  --data-file "outputs/gemini_templates/gemini_zen_et_minimaliste/scraped_data.json" \
  --theme "énergique et coloré"

python -m scripts.gemini_template_generator \
  --data-file "outputs/gemini_templates/gemini_zen_et_minimaliste/scraped_data.json" \
  --theme "naturel et apaisant"

# 3. Montrer les 3 versions au client et il choisit son préféré
```

---

**Ready to generate! 🎨**
