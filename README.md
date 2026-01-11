# 🤖 Agent de Prospection Automatisée

Système automatisé pour générer des propositions de sites web personnalisées et contacter des prospects par email.

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Installation](#installation)
- [Configuration](#configuration)
- [Mode Test (recommandé pour commencer)](#mode-test)
- [Utilisation complète](#utilisation)
- [Modules individuels](#modules-individuels)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Vue d'ensemble

Ce système permet de :
1. 🔍 Scraper Google Maps pour trouver des prospects
2. 🌐 Analyser leurs sites web existants (qualité, modernité)
3. 🎨 Générer des propositions de nouveaux designs modernes
4. 📄 Créer des PDFs de présentation professionnels
5. 📧 Envoyer des emails personnalisés automatiquement

**Fonctionnalités :**
- **Mode Test** : Analyser des sites sans envoyer d'emails (idéal pour commencer)
- Analyse de qualité : score 0-100 pour évaluer si un site est daté
- Supporte les clients AVEC et SANS site web
- Extraction automatique de couleurs depuis les logos
- Génération de contenu par IA (Claude) pour clients sans site
- Templates HTML personnalisables par secteur (beauté, artisan, restauration, santé, commerce)
- Screenshots automatiques (desktop + mobile)
- PDFs professionnels avec avant/après
- Gestion des proxies et SSL (compatible environnements d'entreprise)

---

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/AGENT.git
cd AGENT
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
playwright install chromium
```

**Note :** L'installation de Playwright peut prendre quelques minutes.

---

## ⚙️ Configuration

### 1. Copier le fichier d'environnement

```bash
cp .env.example .env
```

### 2. Éditer `.env` avec vos clés API

Ouvrez `.env` et remplissez selon vos besoins :

#### 🔵 Pour le MODE TEST (analyse uniquement, pas d'emails)

Configuration minimale - aucune clé API nécessaire ! Juste :

```env
# Rien de spécial à configurer pour le mode test
# Optionnel : proxy si vous êtes en entreprise
HTTP_PROXY=
HTTPS_PROXY=
VERIFY_SSL=true
```

#### 🔴 Pour le MODE COMPLET (avec envoi d'emails)

##### Gmail (recommandé pour commencer)

```env
GMAIL_ADDRESS=votre-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
FROM_NAME=Votre Nom
```

**Comment obtenir un App Password Gmail :**
1. Activer la validation en 2 étapes sur votre compte Google
2. Aller sur https://myaccount.google.com/apppasswords
3. Créer un mot de passe d'application pour "Mail"
4. Copier le code à 16 caractères

> **Voir GMAIL_SETUP.md pour un guide détaillé**

**Limites Gmail :** 500/jour max, mais pour du cold email on recommande **20-30 emails/jour maximum**

#### 🟡 OPTIONNEL - Claude AI (uniquement pour clients SANS site)

```env
ANTHROPIC_API_KEY=sk-ant-votre_cle_anthropic_ici
USE_AI_FOR_NO_SITE=true
```

**Comment obtenir la clé Claude :**
1. Créer un compte sur [Anthropic Console](https://console.anthropic.com)
2. Aller dans Settings → API Keys
3. Créer une nouvelle clé
4. Ajouter des crédits ($5 minimum)

**Si vous ne voulez PAS utiliser l'IA :** Mettez `USE_AI_FOR_NO_SITE=false`

#### 🌐 OPTIONNEL - Proxy (si vous êtes sur un PC d'entreprise)

Si vous avez des erreurs de connexion, configurez le proxy :

```env
HTTP_PROXY=http://proxy.entreprise.com:8080
HTTPS_PROXY=http://proxy.entreprise.com:8080
```

#### 🔒 OPTIONNEL - SSL (si erreurs de certificats)

Si vous avez des erreurs SSL :

```env
VERIFY_SSL=false
```

⚠️ **Attention :** Désactiver SSL n'est pas sécurisé. À utiliser uniquement en dernier recours.

### 3. Vérifier la configuration

```bash
# Test rapide de la configuration
python scripts/quick_test.py
```

Vous devriez voir :
```
✅ PASS - Configuration
✅ PASS - Analyseur de sites
✅ PASS - Génération HTML
🎉 TOUS LES TESTS SONT PASSÉS !
```

---

## 🧪 Mode Test

**👉 RECOMMANDÉ POUR COMMENCER**

Le mode test permet d'**analyser des sites web et générer des propositions SANS envoyer d'emails**.

### Pourquoi commencer par le mode test ?

1. ✅ Aucune configuration email nécessaire
2. ✅ Voir la qualité des sites générés
3. ✅ Tester sur votre propre secteur
4. ✅ Valider les templates avant prospection

### Utilisation

```bash
# Analyser 3 coiffeurs à Paris
python scripts/test_analysis.py --secteur "coiffeur" --ville "Paris" --limite 3

# Analyser 5 restaurants à Lyon
python scripts/test_analysis.py --secteur "restaurant" --ville "Lyon" --limite 5
```

### Ce qui se passe

```
📍 Recherche Google Maps
   └─ Trouve 5 établissements

🔄 Pour chaque établissement :
   ├─ Scrape le site existant
   ├─ 📊 ANALYSE DE QUALITÉ (score /100)
   │   ├─ HTML5 structure
   │   ├─ Responsive design
   │   ├─ Modernité CSS
   │   └─ Qualité contenu
   ├─ Extrait couleurs du logo
   ├─ Génère version améliorée
   └─ Screenshots avant/après

📊 Rapport d'analyse détaillé
   ├─ Score de chaque site
   ├─ % de sites datés
   └─ Opportunités détectées
```

### Résultats générés

```
outputs/
├── html/
│   ├── test_001_generated.html      # Nouveau design #1
│   └── test_002_generated.html      # Nouveau design #2
├── screenshots/
│   ├── test_001_generated_desktop.png
│   └── test_001_generated_mobile.png
├── temp/
│   └── test_001/
│       └── screenshot_original.png   # Site original (AVANT)
└── report/
    └── analyse_coiffeur_Paris_*.txt  # Rapport détaillé
```

### Exemple de rapport

```
Prospect 1/5: Salon Beauté Parisienne

Score: 42/100
Qualité: Moyen (design daté)
Site daté: OUI ⚠️
Recommandation: Site daté, refonte visuelle recommandée

⚠️ Problèmes détectés:
  • Structure HTML obsolète (pas de tags sémantiques)
  • Pas de meta viewport (site non-responsive)
  • Pas de media queries (design fixe)

✅ Points forts:
  • Logo présent
  • 5 images de qualité

📁 Fichiers générés:
   HTML: outputs/html/test_001_generated.html
   Screenshot original: outputs/temp/test_001/screenshot_original.png
   Screenshot nouveau: outputs/screenshots/test_001_generated_desktop.png
```

> **📖 Voir TEST_MODE.md pour plus de détails sur les critères d'analyse**

---

## 🎮 Utilisation complète

### Mode complet (recommandé)

Lance tout le pipeline automatiquement :

```bash
python scripts/main.py --secteur "coiffeur" --ville "Paris" --limite 50
```

**Paramètres :**
- `--secteur` : Type d'établissement (coiffeur, restaurant, plombier, etc.)
- `--ville` : Ville de recherche
- `--limite` : Nombre maximum de prospects (max 50/jour recommandé)

**Exemples :**

```bash
# 50 coiffeurs à Paris
python scripts/main.py --secteur "coiffeur" --ville "Paris" --limite 50

# 30 restaurants à Lyon
python scripts/main.py --secteur "restaurant" --ville "Lyon" --limite 30

# 10 plombiers à Marseille (test)
python scripts/main.py --secteur "plombier" --ville "Marseille" --limite 10
```

### Ce qui se passe automatiquement :

```
📍 Scraping Google Maps → 50 établissements trouvés
   ├─ 30 avec site web
   └─ 20 sans site web

🔄 Traitement de chaque prospect :
   ├─ Scraping du site (si existe)
   ├─ Extraction couleurs du logo
   ├─ Génération HTML personnalisé
   ├─ Screenshots (desktop + mobile)
   ├─ Création PDF (3 pages)
   └─ Envoi email avec PDF

📊 Rapport final généré
   └─ outputs/reports/rapport_2025-01-10_09-50.txt
```

**Durée estimée :** 40-50 sec par prospect = **~35-40 min pour 50 prospects**

---

## 🔧 Modules individuels (pour debug)

Vous pouvez tester chaque module séparément :

### 1. Scraper Google Maps uniquement

```bash
python scripts/main.py --segment google-maps --secteur "coiffeur" --ville "Paris" --limite 10
```

Résultat : fichier CSV dans `data/prospects/`

**Test standalone :**
```bash
python scripts/modules/google_maps_scraper.py --query "coiffeur" --city "Paris" --max 5
```

### 2. Scraper un site web

```bash
python scripts/modules/website_scraper.py --url "https://exemple-coiffeur.fr" --client-id "test001"
```

Résultat : données JSON + images téléchargées dans `temp/client_test001/`

### 3. Extraire les couleurs d'un logo

```bash
python scripts/modules/color_extractor.py --logo "temp/client_001/logo.png"
```

Résultat : palette de couleurs affichée + preview HTML

### 4. Générer du contenu avec IA

```bash
python scripts/modules/content_generator.py --name "Salon Marie" --category "Salon de coiffure" --city "Paris"
```

Résultat : contenu JSON généré

### 5. Générer un HTML

```bash
python scripts/modules/html_generator.py --sector "beaute" --client-id "test"
```

Résultat : fichier HTML dans `temp/client_test/`

### 6. Prendre des screenshots

```bash
python scripts/modules/screenshot_maker.py --html "temp/client_001/website_generated.html" --client-id "001"
```

Résultat : PNG desktop + mobile dans `outputs/screenshots/`

### 7. Générer un PDF

```bash
python scripts/modules/pdf_generator.py \
  --client-id "001" \
  --desktop "outputs/screenshots/client_001_generated_desktop.png" \
  --mobile "outputs/screenshots/client_001_generated_mobile.png" \
  --name "Salon Test"
```

Résultat : PDF dans `outputs/pdfs/`

### 8. Envoyer un email de test

```bash
python scripts/modules/email_sender.py \
  --to "votre-email-test@gmail.com" \
  --pdf "outputs/pdfs/proposition_client_001.pdf" \
  --name "Salon Test" \
  --has-website
```

---

## 📁 Structure du projet

```
AGENT/
├── config/
│   └── settings.py              # Configuration centrale
├── scripts/
│   ├── main.py                  # Script principal (pipeline complet)
│   ├── test_analysis.py         # 🆕 Mode test (analyse sans emails)
│   ├── quick_test.py            # 🆕 Test de configuration
│   ├── modules/                 # Modules fonctionnels
│   │   ├── google_maps_scraper.py
│   │   ├── website_scraper.py
│   │   ├── website_analyzer.py  # 🆕 Analyse qualité sites
│   │   ├── color_extractor.py
│   │   ├── content_generator.py
│   │   ├── html_generator.py
│   │   ├── screenshot_maker.py
│   │   ├── pdf_generator.py
│   │   └── email_sender.py      # ✏️ Migré de SendGrid vers Gmail
│   └── utils/                   # Utilitaires
│       ├── logger.py
│       └── file_manager.py
├── templates/                   # Templates HTML par secteur
│   ├── beaute/
│   ├── artisan/
│   ├── restauration/
│   ├── sante/
│   └── commerce/
├── data/
│   └── prospects/               # Fichiers CSV des prospects
├── outputs/
│   ├── html/                    # Sites HTML générés
│   ├── screenshots/             # Screenshots générés
│   ├── pdfs/                    # PDFs créés
│   └── reports/                 # Rapports d'exécution et d'analyse
├── temp/                        # Fichiers temporaires (auto-nettoyés)
├── .env                         # Configuration (À CRÉER)
├── .env.example                 # Template de configuration
├── requirements.txt             # Dépendances Python
├── README.md                    # Ce fichier
├── TEST_MODE.md                 # 🆕 Guide du mode test
├── GMAIL_SETUP.md               # 🆕 Guide configuration Gmail
└── CONFIGURATION.md             # Guide de configuration détaillé
```

---

## 🐛 Troubleshooting

### Erreur : "GMAIL_ADDRESS manquante" ou "GMAIL_APP_PASSWORD manquante"

✅ **Solution :**
1. Vérifiez que `.env` existe et contient `GMAIL_ADDRESS` et `GMAIL_APP_PASSWORD`
2. Consultez `GMAIL_SETUP.md` pour créer un App Password
3. Si vous voulez juste tester, utilisez le mode test (pas besoin d'email)

### Erreur : "Timeout lors de la recherche Google Maps"

✅ **Solutions :**
1. Ajoutez `--headless` pour désactiver le mode headless (plus lent mais plus stable)
2. Vérifiez votre connexion Internet
3. Si vous êtes derrière un proxy, configurez `HTTP_PROXY` dans `.env`

### Erreur : "SSL: CERTIFICATE_VERIFY_FAILED"

✅ **Solutions :**
1. Dans `.env`, ajoutez `VERIFY_SSL=false`
2. Si sur PC entreprise, configurez le proxy

### Erreur : "Playwright executable doesn't exist"

✅ **Solution :**
```bash
playwright install chromium
```

### Les emails arrivent en spam

✅ **Solutions :**
1. Configurez SPF, DKIM, DMARC sur votre domaine (voir doc SendGrid)
2. Limitez à 50 emails/jour maximum
3. "Warm-up" progressif : 10/jour puis 20/jour puis 50/jour
4. Utilisez un domaine professionnel (pas @gmail.com)

### Module IA ne fonctionne pas

✅ **Solutions :**
1. Vérifiez que `ANTHROPIC_API_KEY` est dans `.env`
2. Vérifiez que vous avez des crédits sur votre compte Anthropic
3. Si vous ne voulez pas l'IA : `USE_AI_FOR_NO_SITE=false` (seuls les clients avec site seront contactés)

### Erreur : "Module not found"

✅ **Solution :**
```bash
# Réinstaller les dépendances
pip install -r requirements.txt
```

---

## 💰 Coûts estimés

| Service | Coût | Note |
|---------|------|------|
| **Gmail SMTP** | Gratuit | Jusqu'à 500 emails/jour (20-30 recommandés pour cold email) |
| **Claude API** | $0.60 | Pour 20 clients SANS site (optionnel) |
| **Total pour 30 prospects/jour** | **$0.30-0.60** | Quasi gratuit ! |

> **Mode test :** Complètement gratuit (pas d'envoi d'emails, pas d'API)

---

## 📊 Résultats attendus

**Sur 50 prospects contactés :**
- Taux d'ouverture : **30-40%** (15-20 emails ouverts)
- Taux de lecture PDF : **60%** des ouvertures (9-12 PDFs lus)
- Taux de réponse : **10-15%** (5-7 réponses)
- Conversions en clients : **30-40%** des réponses (2-3 clients)

**Taux de conversion global : ~4-6%** (excellent pour du cold email !)

---

## 🔐 Sécurité

⚠️ **Important :**
- Ne jamais commit le fichier `.env` (déjà dans `.gitignore`)
- Ne pas partager vos clés API
- Les données prospects contiennent des infos personnelles → ne pas les versionner

---

## 📞 Support

Pour toute question ou problème :
1. Vérifiez la section [Troubleshooting](#troubleshooting)
2. Lancez les modules en mode debug individuellement
3. Consultez les logs dans `outputs/reports/agent_YYYY-MM-DD.log`

---

## 🎯 Prochaines étapes

1. **Testez sur 5-10 prospects** pour valider le système
2. **Analysez les premiers retours** et ajustez les templates/emails
3. **Montez progressivement à 50/jour** pour warm-up de la réputation email
4. **Mesurez les résultats** et optimisez

Bon prospecting ! 🚀
