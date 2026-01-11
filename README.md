# 🤖 Agent de Prospection Automatisée

Système automatisé pour générer des propositions de sites web personnalisées et contacter des prospects par email.

## 📋 Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Modules individuels](#modules-individuels)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Vue d'ensemble

Ce système permet de :
1. 🔍 Scraper Google Maps pour trouver des prospects
2. 🌐 Analyser leurs sites web (s'ils en ont)
3. 🎨 Générer des propositions de nouveaux designs
4. 📄 Créer des PDFs de présentation
5. 📧 Envoyer des emails personnalisés automatiquement

**Fonctionnalités :**
- Supporte les clients AVEC et SANS site web
- Extraction automatique de couleurs depuis les logos
- Génération de contenu par IA (Claude) pour clients sans site
- Templates HTML personnalisables par secteur
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

Ouvrez `.env` et remplissez **OBLIGATOIREMENT** :

#### 🔴 OBLIGATOIRE - SendGrid (pour les emails)

```env
SENDGRID_API_KEY=SG.votre_cle_sendgrid_ici
FROM_EMAIL=votre-email@votreentreprise.com
FROM_NAME=Votre Nom
```

**Comment obtenir la clé SendGrid :**
1. Créer un compte sur [SendGrid](https://sendgrid.com)
2. Aller dans Settings → API Keys
3. Créer une nouvelle clé avec permissions "Full Access"
4. Copier la clé (elle ne sera montrée qu'une fois !)

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
python config/settings.py
```

Vous devriez voir :
```
✅ Configuration valide !
📧 Email: votre-email@votreentreprise.com
🎯 Max prospects/jour: 50
...
```

---

## 🎮 Utilisation

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
│   ├── main.py                  # Script principal
│   ├── modules/                 # Modules fonctionnels
│   │   ├── google_maps_scraper.py
│   │   ├── website_scraper.py
│   │   ├── color_extractor.py
│   │   ├── content_generator.py
│   │   ├── html_generator.py
│   │   ├── screenshot_maker.py
│   │   ├── pdf_generator.py
│   │   └── email_sender.py
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
│   ├── screenshots/             # Screenshots générés
│   ├── pdfs/                    # PDFs créés
│   └── reports/                 # Rapports d'exécution
├── temp/                        # Fichiers temporaires (auto-nettoyés)
├── .env                         # Configuration (À CRÉER)
├── .env.example                 # Template de configuration
├── requirements.txt             # Dépendances Python
└── README.md                    # Ce fichier
```

---

## 🐛 Troubleshooting

### Erreur : "SENDGRID_API_KEY manquante"

✅ **Solution :** Vérifiez que `.env` existe et contient `SENDGRID_API_KEY=...`

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
| **SendGrid** | Gratuit | Jusqu'à 100 emails/jour |
| **Claude API** | $0.60 | Pour 20 clients SANS site (optionnel) |
| **Total pour 50 prospects/jour** | **$0.60** | Quasi gratuit ! |

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
