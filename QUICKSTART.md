# ⚡ Démarrage Rapide

Guide ultra-rapide pour lancer votre premier test en 10 minutes.

## 📝 Checklist avant de commencer

- [ ] Python 3.8+ installé
- [ ] Compte SendGrid créé (gratuit)
- [ ] (Optionnel) Compte Anthropic/Claude créé

---

## 🚀 Installation (5 minutes)

### 1. Cloner et installer

```bash
git clone https://github.com/votre-username/AGENT.git
cd AGENT
pip install -r requirements.txt
playwright install chromium
```

### 2. Configuration minimale

```bash
cp .env.example .env
nano .env  # ou votre éditeur préféré
```

**Remplissez AU MINIMUM :**
```env
SENDGRID_API_KEY=SG.votre_cle_ici
FROM_EMAIL=vous@votreentreprise.com
FROM_NAME=Votre Nom
```

### 3. Tester la configuration

```bash
python config/settings.py
```

Vous devez voir : `✅ Configuration valide !`

---

## 🧪 Premier test (5 min)

### Test avec 5 prospects

```bash
python scripts/main.py --secteur "coiffeur" --ville "Paris" --limite 5
```

**Ce qui va se passer :**
1. Recherche de 5 coiffeurs à Paris sur Google Maps (30 sec)
2. Traitement de chaque prospect (40 sec chacun = 3-4 min)
3. Génération d'un rapport

**Résultats :**
- PDFs générés dans `outputs/pdfs/`
- Emails envoyés (si emails trouvés)
- Rapport dans `outputs/reports/`

---

## 🔍 Tester module par module

Si le test complet ne fonctionne pas, testez chaque module :

### 1. Google Maps (30 sec)

```bash
python scripts/modules/google_maps_scraper.py \
  --query "coiffeur" \
  --city "Paris" \
  --max 3
```

✅ Doit afficher 3 établissements avec leurs infos

### 2. Scraper un site (30 sec)

```bash
python scripts/modules/website_scraper.py \
  --url "https://www.exemple-coiffeur.fr" \
  --client-id "test"
```

✅ Doit créer `temp/client_test/` avec images et données

### 3. Générer du contenu IA (5 sec)

**⚠️ Nécessite ANTHROPIC_API_KEY dans .env**

```bash
python scripts/modules/content_generator.py \
  --name "Salon Test" \
  --category "Salon de coiffure" \
  --city "Paris"
```

✅ Doit afficher un slogan, services, etc.

### 4. Envoyer un email de test (2 sec)

**D'abord, créez un PDF de test :**

```bash
python scripts/modules/pdf_generator.py \
  --client-id "test" \
  --desktop "chemin/vers/image.png" \
  --name "Test"
```

**Puis envoyez :**

```bash
python scripts/modules/email_sender.py \
  --to "votre-email@example.com" \
  --pdf "outputs/pdfs/proposition_client_test.pdf" \
  --name "Salon Test"
```

✅ Vous devez recevoir l'email

---

## ❌ Problèmes courants

### "SENDGRID_API_KEY manquante"
→ Vérifiez `.env`, la clé doit commencer par `SG.`

### "Timeout Google Maps"
→ Ajoutez `--headless` à la commande :
```bash
python scripts/modules/google_maps_scraper.py --query "coiffeur" --city "Paris" --max 3 --headless
```

### "Playwright not found"
→ Réinstallez :
```bash
playwright install chromium
```

### "SSL Error"
→ Dans `.env` :
```env
VERIFY_SSL=false
```

---

## 📧 Configuration email avancée (éviter les spams)

### 1. Vérifier votre domaine sur SendGrid

1. Aller sur SendGrid → Settings → Sender Authentication
2. Cliquer "Authenticate Your Domain"
3. Ajouter les DNS records fournis chez votre registrar

### 2. Warm-up progressif

**Jour 1-3 :** 10 emails/jour
```bash
python scripts/main.py --secteur "coiffeur" --ville "Paris" --limite 10
```

**Jour 4-7 :** 20 emails/jour
```bash
python scripts/main.py --secteur "coiffeur" --ville "Lyon" --limite 20
```

**Jour 8+ :** 50 emails/jour
```bash
python scripts/main.py --secteur "coiffeur" --ville "Marseille" --limite 50
```

---

## 🎯 Prochaines étapes

✅ **Test réussi avec 5 prospects ?**

Passez à :
1. Testez avec 10-20 prospects
2. Analysez les réponses
3. Ajustez les templates HTML si besoin (`templates/beaute/template_1.html`)
4. Personnalisez les emails (`scripts/modules/email_sender.py`)
5. Montez à 50/jour

**Besoin d'aide ?** → Consultez `README.md` pour la documentation complète

---

## 🔥 Mode production

Une fois validé, automatisez avec cron (Linux/Mac) :

```bash
crontab -e
```

Ajoutez :
```cron
# Lancer à 9h du lundi au vendredi
0 9 * * 1-5 cd /chemin/vers/AGENT && python scripts/main.py --secteur "coiffeur" --ville "Paris" --limite 50
```

Le système tournera automatiquement chaque matin ! 🚀

---

**Temps total : ~10 minutes**
**Vous êtes prêt à lancer votre première campagne !**
