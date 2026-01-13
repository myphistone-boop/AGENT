# 🚀 Quick Start - Générateur Gemini

Système pour générer des sites web créatifs à partir de sites existants.

## Installation rapide

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Configurer la clé API Gemini
export GEMINI_API_KEY="votre_clé_api"
# Obtenir une clé: https://makersuite.google.com/app/apikey
```

## Utilisation

### Commande basique

```bash
python -m scripts.gemini_template_generator \
  --url "https://site-a-scraper.com" \
  --theme "thérapeute"
```

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

## Workflow

1. **Scrape** un site existant (URL)
2. **Gemini génère** un nouveau site créatif du même thème
3. **Validation manuelle** du résultat
4. **Déploiement** si validé

## Coûts

- **Gemini Pro**: ~$0.03-0.05 par site
- **Gemini Flash**: ~$0.002-0.003 par site

Pour 100 sites: ~$0.20-0.30 avec Flash

## Documentation complète

Voir: [`docs/GEMINI_TEMPLATE_GENERATOR.md`](docs/GEMINI_TEMPLATE_GENERATOR.md)

## Exemples

```bash
# Thérapeute
python -m scripts.gemini_template_generator --url "https://psy.com" --theme "thérapeute" --preview

# Coach sportif
python -m scripts.gemini_template_generator --url "https://coach.com" --theme "coach sportif" --preview

# Yoga
python -m scripts.gemini_template_generator --url "https://yoga.com" --theme "yoga" --preview
```

---

**Ready to generate! 🎨**
