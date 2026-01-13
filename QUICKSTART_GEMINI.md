# 🚀 Quick Start - Générateur Gemini

Système pour générer des sites web créatifs à partir de sites existants.

## 🎯 Comment ça marche

**"Même squelette, nouveau visuel"** - Le client reconnaît son site mais en mieux !

1. **Scrape** → Extrait la structure COMPLÈTE du site (ordre, sections, tous les textes)
2. **Gemini** → Recrée le MÊME squelette avec un design moderne
3. **HTML généré** → Mêmes contenus + Vraies images + Design professionnel
4. **Validation** → Le client voit "son site mais magnifique"

**Préservé exactement :**
- ✅ Ordre des sections
- ✅ Tous les titres (texte identique)
- ✅ Tous les paragraphes (texte identique)
- ✅ Toutes les listes
- ✅ Images originales (URLs)

**Changé (design uniquement) :**
- 🎨 Couleurs modernes
- 🎨 Typographie élégante
- 🎨 Layout contemporain
- 🎨 Animations fluides

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

### Commande basique (avec scraping)

```bash
python -m scripts.gemini_template_generator \
  --url "https://site-a-scraper.com" \
  --theme "thérapeute"
```

### Régénération sans rescraper (skip phase 1)

Si vous avez déjà scrappé un site, vous pouvez régénérer sans rescraper:

```bash
# Aller directement à la phase 2 (Gemini) avec les données existantes
python -m scripts.gemini_template_generator \
  --data-file "temp_files/gemini_therapeute/scraped_data.json" \
  --theme "thérapeute"
```

**Avantages:**
- ⚡ Plus rapide (pas de scraping)
- 🔄 Régénérer plusieurs fois avec Gemini
- 💰 Économise les requêtes de scraping

**Cas d'usage:**
- Tester différents thèmes avec les mêmes données
- Régénérer après avoir ajusté le prompt Gemini
- Éviter de scraper le même site plusieurs fois

### Avec prévisualisation automatique

```bash
python -m scripts.gemini_template_generator \
  --url "https://site-a-scraper.com" \
  --theme "thérapeute" \
  --preview
```

## Résultat

Fichiers générés dans: `outputs/gemini_templates/gemini_therapeute/`

```
gemini_therapeute/
├── index.html           # Site complet (HTML/CSS/JS)
├── scraped_data.json    # Données extraites
└── README.md            # Guide de validation
```

## 📂 Stockage des fichiers

### Fichiers temporaires de scraping
```
temp_files/gemini_therapeute/
├── screenshot_original.png    # Capture d'écran du site original
└── scraped_data.json          # Données brutes extraites
```
**Note:** Ces fichiers temporaires sont créés pendant le scraping et peuvent être supprimés après génération.

### Fichiers générés (sortie finale)
```
outputs/gemini_templates/gemini_therapeute/
├── index.html           # Site complet généré par Gemini
├── scraped_data.json    # Données extraites (pour référence)
└── README.md            # Guide de validation manuelle
```
**Note:** C'est le dossier final contenant votre template généré prêt pour validation.

## Workflow

### Mode complet (avec scraping)
1. **Scrape** un site existant (URL)
2. **Gemini génère** un nouveau site créatif du même thème
3. **Validation manuelle** du résultat
4. **Déploiement** si validé

### Mode rapide (sans rescraper)
1. ~~**Scrape**~~ → **Utiliser les données existantes** (skip phase 1)
2. **Gemini génère** un nouveau site créatif
3. **Validation manuelle** du résultat
4. **Déploiement** si validé

## Coûts

- **Gemini Pro**: ~$0.03-0.05 par site
- **Gemini Flash**: ~$0.002-0.003 par site

Pour 100 sites: ~$0.20-0.30 avec Flash

## Documentation complète

Voir: [`docs/GEMINI_TEMPLATE_GENERATOR.md`](docs/GEMINI_TEMPLATE_GENERATOR.md)

## Exemples

### Première génération (avec scraping)

```bash
# Thérapeute
python -m scripts.gemini_template_generator --url "https://psy.com" --theme "thérapeute" --preview

# Coach sportif
python -m scripts.gemini_template_generator --url "https://coach.com" --theme "coach sportif" --preview

# Yoga
python -m scripts.gemini_template_generator --url "https://yoga.com" --theme "yoga" --preview
```

### Régénération rapide (sans rescraper)

```bash
# Régénérer avec un thème différent
python -m scripts.gemini_template_generator \
  --data-file "outputs/gemini_templates/gemini_therapeute/scraped_data.json" \
  --theme "coach de vie"

# Tester plusieurs thèmes rapidement
python -m scripts.gemini_template_generator \
  --data-file "temp_files/gemini_yoga/scraped_data.json" \
  --theme "méditation et bien-être"
```

---

**Ready to generate! 🎨**
