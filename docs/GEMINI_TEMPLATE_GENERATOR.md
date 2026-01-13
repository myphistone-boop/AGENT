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

### Images et contenus

Le système utilise les **vraies URLs** des images du site source :
- ✅ Logo du site original
- ✅ Images du site original (URLs directes)
- ✅ Textes extraits du site
- ✅ Informations de contact (téléphone, email)

**Avantages :**
- Pas de stockage local nécessaire
- Images en haute qualité depuis la source
- Génération ultra-rapide
- Coût minimal

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

```
outputs/gemini_templates/gemini_therapeute/
├── index.html              # Site complet (HTML/CSS/JS)
├── scraped_data.json       # Données extraites du site source
└── README.md               # Guide de validation
```

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

### Erreur: "Clé API Gemini manquante"

```bash
export GEMINI_API_KEY="votre_clé"
# Ou ajouter au .env
```

### Erreur de scraping (site protégé)

Certains sites bloquent les scrapers. Solutions:
- Utiliser un proxy (configurer dans `config.py`)
- Désactiver SSL verification si certificat invalide

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

**Site source:** Site WordPress basique de thérapeute
**Généré:** One-page moderne avec:
- Hero section avec dégradé
- Animations au scroll
- Design épuré et professionnel
- Palette harmonieuse
- Formulaire de contact intégré

**Temps de génération:** ~30-60 secondes
**Coût:** $0.03-0.05

---

## 📞 Support

Pour des questions ou problèmes:
1. Vérifier la section Troubleshooting ci-dessus
2. Vérifier les logs dans la console
3. Tester avec un site simple d'abord

---

**Happy generating! 🚀**
