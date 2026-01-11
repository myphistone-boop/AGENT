# Mode Test - Analyse de Secteur

Ce mode permet de **tester la capacité du système à analyser des sites web et à générer de belles pages d'accueil** sans envoyer d'emails.

## 🎯 Objectif

Analyser un secteur d'activité pour :
1. ✅ Trouver des sites web de professionnels
2. ✅ Évaluer si ces sites sont modernes ou datés
3. ✅ Récupérer leurs informations (couleurs, logo, contenu)
4. ✅ Générer une belle page d'accueil améliorée
5. ✅ Créer des screenshots avant/après pour comparaison

**AUCUN EMAIL N'EST ENVOYÉ** - C'est uniquement pour tester et valider la génération de sites.

## 🚀 Utilisation

### Installation des dépendances

```bash
pip install -r requirements.txt
playwright install chromium
```

### Configuration minimale

Créez un fichier `.env` :

```env
# === PROXIES (si nécessaire en entreprise) ===
HTTP_PROXY=
HTTPS_PROXY=
VERIFY_SSL=true

# === IA (optionnel - pour clients sans site web) ===
ANTHROPIC_API_KEY=sk-ant-xxxxx
USE_AI_FOR_NO_SITE=true
```

> **Note**: L'API Anthropic n'est nécessaire que si vous voulez générer du contenu IA pour les clients **sans site web**. Pour analyser des sites existants, ce n'est pas requis.

### Lancer une analyse

```bash
# Analyser 5 coiffeurs à Paris
python scripts/test_analysis.py --secteur "coiffeur" --ville "Paris" --limite 5

# Analyser 3 restaurants à Lyon
python scripts/test_analysis.py --secteur "restaurant" --ville "Lyon" --limite 3

# Analyser 10 plombiers à Marseille
python scripts/test_analysis.py --secteur "plombier" --ville "Marseille" --limite 10
```

## 📊 Ce que fait le script

### 1. Recherche sur Google Maps
- Trouve des établissements du secteur dans la ville spécifiée
- Récupère : nom, adresse, téléphone, site web, catégorie, notes

### 2. Pour chaque site web trouvé

**Scraping du site :**
- Capture screenshot original (AVANT)
- Extrait : logo, couleurs, images, textes, téléphone, email

**Analyse de qualité :**
- Évalue la modernité du site (score /100)
- Détecte les problèmes : design daté, structure obsolète, etc.
- Identifie les points forts : responsive, animations CSS, etc.

**Génération d'une version améliorée :**
- Utilise les couleurs extraites du logo
- Sélectionne un template moderne adapté au secteur
- Génère HTML/CSS responsive avec gradients
- Capture screenshot nouveau design (APRÈS)

### 3. Rapport d'analyse

Le script génère un rapport détaillé avec :
- Score de qualité de chaque site (/100)
- Liste des problèmes détectés
- Recommandations
- Statistiques globales (% de sites datés)
- Fichiers HTML et screenshots générés

## 📁 Structure des fichiers générés

```
outputs/
├── html/
│   ├── test_001_generated.html      # Site amélioré #1
│   ├── test_002_generated.html      # Site amélioré #2
│   └── ...
├── screenshots/
│   ├── test_001_generated_desktop.png   # Screenshot APRÈS (desktop)
│   ├── test_001_generated_mobile.png    # Screenshot APRÈS (mobile)
│   └── ...
├── temp/
│   └── test_001/
│       ├── screenshot_original.png      # Screenshot AVANT
│       ├── logo.png                     # Logo extrait
│       └── images/                      # Images extraites
└── report/
    ├── analyse_coiffeur_Paris_20260111_143022.txt   # Rapport texte
    └── analyse_coiffeur_Paris_20260111_143022.json  # Données JSON
```

## 📊 Exemple de sortie

```
================================================================================
🔍 ANALYSE DE SECTEUR - MODE TEST
================================================================================
Secteur: coiffeur
Ville: Paris
Limite: 5 prospects
================================================================================

📍 ÉTAPE 1/3 : Recherche sur Google Maps
========================================================================

🔍 Recherche: coiffeur à Paris

📊 Trouvés:
   Total: 5
   Avec site web: 4
   Sans site web: 1

🔄 ÉTAPE 2/3 : Analyse et génération (5 prospects)
========================================================================

──────────────────────────────────────────────────────────────────────────
Prospect 1/5: Salon Beauté Parisienne
──────────────────────────────────────────────────────────────────────────
Type: AVEC site web
URL: https://salonbeaute.fr
Catégorie: Salon de coiffure
Secteur détecté: beaute

🌐 Scraping et analyse du site...
🔍 Analyse de la qualité...
🎨 Extraction couleurs du logo...
✨ Génération d'une version améliorée...
📸 Capture screenshots (avant/après)...

──────────────────────────────────────────────────────────────────────────
📊 RÉSULTATS D'ANALYSE:
──────────────────────────────────────────────────────────────────────────
Score: 42/100
Qualité: Moyen (design daté)
Site daté: OUI ⚠️
Recommandation: Site daté, refonte visuelle recommandée

✅ Points forts:
   • Logo présent
   • 5 images de qualité

⚠️  Problèmes (7):
   • Structure HTML obsolète (pas de tags sémantiques)
   • Pas de meta viewport (site non-responsive)
   • Pas de media queries (design fixe)
   • Pas de description/slogan

📁 Fichiers générés:
   HTML: outputs/html/test_001_generated.html
   Screenshot original: outputs/temp/test_001/screenshot_original.png
   Screenshot nouveau: outputs/screenshots/test_001_generated_desktop.png

[...]

📊 ÉTAPE 3/3 : Génération du rapport d'analyse
========================================================================

================================================================================
RAPPORT D'ANALYSE DE SECTEUR
================================================================================

Prospects trouvés:        5
  - Avec site web:        4
  - Sans site web:        1

Analyse des sites:
  - Sites modernes:       1
  - Sites datés:          3

Sites générés:            5

Taux de sites datés: 75.0%
Opportunités détectées: 3 sites nécessitant une refonte
```

## 🎨 Critères d'analyse

Le système évalue la qualité des sites web selon :

| Critère | Points | Description |
|---------|--------|-------------|
| **Structure HTML5** | 10 pts | Tags sémantiques (header, nav, section, etc.) |
| **Responsive design** | 15 pts | Meta viewport, media queries, flexbox/grid |
| **Design moderne** | 15 pts | Dégradés CSS, animations, ombres |
| **Typographie** | 5 pts | Google Fonts, polices modernes |
| **Contenu** | 20 pts | Logo, images de qualité, textes structurés |
| **Technologies modernes** | 20 pts | Frameworks JS, lazy loading, CDN |
| **Performance** | 15 pts | Scripts optimisés, ressources minimisées |

**Total : 100 points**

### Barème de qualité

- **80-100** : Excellent (site moderne)
- **60-79** : Correct (quelques améliorations possibles)
- **40-59** : Moyen (design daté) ⚠️
- **0-39** : Faible (refonte nécessaire) ❌

## 🎯 Templates par secteur

Le système sélectionne automatiquement un template moderne adapté au secteur :

| Secteur | Catégories détectées | Style |
|---------|---------------------|-------|
| **beaute** | Coiffeur, salon, beauté, esthétique | Élégant, dégradés doux |
| **artisan** | Plombier, électricien, menuisier | Professionnel, sobre |
| **restauration** | Restaurant, café, boulangerie, pizzeria | Chaleureux, appétissant |
| **sante** | Médecin, dentiste, kiné, cabinet | Rassurant, propre |
| **commerce** | Autres commerces | Polyvalent, moderne |

Chaque template inclut :
- 🎨 Design responsive (desktop + mobile)
- 🌈 Dégradés CSS modernes
- 📱 Navigation mobile hamburger
- ✨ Animations au scroll
- 🎯 Section hero avec CTA
- 📞 Informations de contact visibles

## 🔧 Personnalisation

Les templates utilisent les **couleurs extraites du logo** du client pour créer une identité visuelle cohérente.

Si aucun logo n'est trouvé, des palettes par défaut adaptées au secteur sont utilisées :
- **Beauté** : Rose/violet élégant
- **Artisan** : Bleu professionnel
- **Restauration** : Orange/rouge chaleureux
- **Santé** : Vert/bleu rassurant
- **Commerce** : Bleu moderne

## 📝 Prochaines étapes

Après avoir testé l'analyse et la génération, vous pourrez :

1. **Valider la qualité** des sites générés
2. **Ajuster les templates** si nécessaire
3. **Passer à la prospection** avec envoi d'emails (script principal)

Pour la prospection complète avec emails, utilisez :
```bash
python scripts/main.py --secteur "coiffeur" --ville "Paris" --limite 50
```

## 🆘 Dépannage

### "Aucun prospect trouvé"
- Vérifiez votre connexion internet
- Essayez une autre ville ou un autre secteur
- Vérifiez les proxies si vous êtes en entreprise

### "Échec du scraping"
- Certains sites bloquent les scrapers (normal)
- Le système continue avec les données Google Maps
- Configurez `VERIFY_SSL=false` si problème de certificat

### "ANTHROPIC_API_KEY manquante"
- Normal si vous analysez des sites existants (pas besoin d'IA)
- Nécessaire uniquement pour générer du contenu pour clients SANS site web
- Configurez dans `.env` ou mettez `USE_AI_FOR_NO_SITE=false`

## 📚 Fichiers du système

| Fichier | Description |
|---------|-------------|
| `scripts/test_analysis.py` | Script principal de test |
| `scripts/modules/website_analyzer.py` | Analyse qualité des sites |
| `scripts/modules/website_scraper.py` | Scraping des sites web |
| `scripts/modules/google_maps_scraper.py` | Recherche Google Maps |
| `scripts/modules/html_generator.py` | Génération HTML/CSS |
| `scripts/modules/color_extractor.py` | Extraction couleurs logos |
| `scripts/modules/screenshot_maker.py` | Capture d'écran |
| `templates/` | Templates HTML par secteur |

---

**Questions ?** Consultez `CONFIGURATION.md` pour plus de détails sur la configuration complète du système.
