# 📧 Configuration Gmail - Guide Complet

## 🎯 Pourquoi un "Mot de passe d'application" ?

Google ne vous laisse PAS utiliser votre mot de passe Gmail normal pour des applications tierces (c'est pour votre sécurité !).

Vous devez créer un **"Mot de passe d'application"** - c'est un mot de passe temporaire spécial juste pour ce projet.

---

## ⚡ Configuration rapide (5 minutes)

### Étape 1 : Activer la validation en 2 étapes (si pas déjà fait)

1. Allez sur https://myaccount.google.com/security
2. Cherchez "Validation en 2 étapes"
3. Cliquez sur "Activer" et suivez les instructions
4. Configurez avec votre téléphone

⚠️ **Sans validation en 2 étapes, vous ne pouvez PAS créer de mot de passe d'application !**

---

### Étape 2 : Créer un mot de passe d'application

1. Allez sur https://myaccount.google.com/apppasswords

   OU

   - Allez sur https://myaccount.google.com/security
   - Cherchez "Mots de passe des applications" (en bas de page)
   - Cliquez dessus

2. **Sélectionnez l'application :**
   - Dans "Sélectionner une application" : choisissez "Autre (nom personnalisé)"
   - Tapez : "Agent Prospection" (ou n'importe quel nom)

3. **Cliquez sur "Générer"**

4. **COPIEZ le mot de passe généré** (format : `xxxx xxxx xxxx xxxx`)

   ⚠️ **IMPORTANT :** Ce mot de passe ne sera montré qu'UNE SEULE FOIS !

---

### Étape 3 : Ajouter dans votre fichier .env

```bash
cd AGENT
nano .env  # ou votre éditeur préféré
```

**Remplissez :**

```env
GMAIL_ADDRESS=votre-email@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
FROM_NAME=Votre Nom
```

**Exemple complet :**

```env
GMAIL_ADDRESS=jean.dupont@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
FROM_NAME=Jean Dupont
```

---

### Étape 4 : Tester la configuration

```bash
python config/settings.py
```

**Vous devez voir :**
```
✅ Configuration valide !
📧 Gmail: jean.dupont@gmail.com
```

---

## 🧪 Test d'envoi d'email

### Créez un PDF de test (si vous n'en avez pas)

```bash
# Créer un fichier texte simple
echo "Test PDF" > test.txt

# Ou créer un vrai PDF de test (nécessite un screenshot)
# Voir README.md pour générer un vrai PDF
```

### Envoyez un email de test à VOUS-MÊME

```bash
python scripts/modules/email_sender.py \
  --to votre-email@gmail.com \
  --pdf chemin/vers/un/fichier.pdf \
  --name "Test Entreprise"
```

**Si ça marche, vous verrez :**
```
✅ Gmail initialisé (votre-email@gmail.com)
📧 Envoi email à: votre-email@gmail.com
✅ Email envoyé avec succès via Gmail
```

**Vérifiez votre boîte de réception !**

---

## ❌ Problèmes courants

### Erreur : "Username and Password not accepted"

**Causes possibles :**

1. **Vous utilisez votre mot de passe Gmail normal** (ne fonctionne pas !)

   ➡️ **Solution :** Utilisez un "Mot de passe d'application"

2. **Validation en 2 étapes pas activée**

   ➡️ **Solution :** Activez-la (voir Étape 1)

3. **Mot de passe d'application mal copié** (espaces manquants ou en trop)

   ➡️ **Solution :** Recopiez exactement `xxxx xxxx xxxx xxxx` avec les espaces

4. **Mauvais email Gmail**

   ➡️ **Solution :** Vérifiez que `GMAIL_ADDRESS` est correct

---

### Erreur : "SMTPAuthenticationError"

```python
❌ Erreur d'authentification Gmail
💡 Vérifiez que vous utilisez un 'Mot de passe d'application' et non votre mot de passe Gmail
```

➡️ **Solution :** Recommencez l'Étape 2 et créez un nouveau mot de passe d'application

---

### Erreur : "Cannot find apppasswords on myaccount"

Cela signifie que la validation en 2 étapes n'est PAS activée.

➡️ **Solution :** Activez d'abord la validation en 2 étapes (Étape 1)

---

### Les emails arrivent en spam chez les destinataires

**C'est normal avec Gmail pour du cold emailing !**

**Solutions :**

1. **Limitez le volume :**
   ```env
   MAX_PROSPECTS_PER_DAY=10  # Au lieu de 50
   ```

2. **Warm-up progressif :**
   - Jour 1-3 : 5 emails/jour
   - Jour 4-7 : 10 emails/jour
   - Jour 8+ : 20 emails/jour max

3. **Ne dépassez JAMAIS 20-30 emails/jour avec Gmail** pour de la prospection

4. **Envoyez d'abord à des gens que vous connaissez** pour "chauffer" le compte

5. **Si taux de spam trop élevé, passez à SendGrid** (voir docs)

---

### Limite atteinte : "Daily sending quota exceeded"

Gmail gratuit = **500 emails/jour MAX**

Mais pour du cold emailing, ne dépassez **JAMAIS 20-30/jour**.

➡️ **Solution :** Configurez `MAX_PROSPECTS_PER_DAY=20` dans `.env`

---

## 🔒 Sécurité

### ⚠️ NE JAMAIS :
- ❌ Partager votre mot de passe d'application
- ❌ Commit le fichier `.env` sur Git (déjà dans `.gitignore`)
- ❌ Envoyer le mot de passe par email/Slack

### ✅ TOUJOURS :
- ✅ Garder le mot de passe dans `.env` uniquement
- ✅ Révoquer les mots de passe d'application non utilisés
- ✅ Créer un nouveau mot de passe si compromis

**Pour révoquer un mot de passe d'application :**
1. https://myaccount.google.com/apppasswords
2. Cliquez sur la corbeille à côté du mot de passe
3. Créez-en un nouveau si besoin

---

## 💡 Astuces

### Utiliser un compte Gmail dédié (recommandé)

Au lieu d'utiliser votre Gmail personnel, créez un compte Gmail juste pour ce projet :

1. Créez `prospection.monentreprise@gmail.com`
2. Activez validation en 2 étapes
3. Créez un mot de passe d'application
4. Utilisez ce compte dans `.env`

**Avantages :**
- Sépare pro/perso
- Si bloqué, votre compte perso n'est pas affecté
- Plus professionnel

---

### Surveiller votre réputation Gmail

Gmail peut bloquer temporairement si :
- Trop d'emails envoyés d'un coup
- Trop de destinataires marquent comme spam
- Taux de bounce trop élevé

**Vérifiez :**
- https://postmaster.google.com (si vous avez un domaine)
- Allez dans Gmail → Paramètres → Comptes et importation → Vérifier si compte bloqué

---

## 📊 Limites Gmail vs SendGrid

| Limite | Gmail Gratuit | SendGrid Gratuit |
|--------|---------------|------------------|
| **Emails/jour** | 500 | 100 |
| **Recommandé pour prospection** | 20-30 | 100 |
| **Risque de spam** | 🔴 Élevé | 🟢 Faible |
| **Risque de blocage** | 🔴 Élevé | 🟢 Faible |
| **Setup** | ✅ 5 min | ⚠️ 15 min + DNS |
| **Coût** | Gratuit | Gratuit |

**Recommandation :**
- **Pour tester (5-20 emails)** : Gmail parfait ✅
- **Pour produire (50+ emails/jour)** : Passez à SendGrid

---

## 🔄 Migration vers SendGrid (plus tard)

Si vous voulez migrer vers SendGrid après avoir testé avec Gmail :

1. Voir le fichier `SENDGRID_MIGRATION.md` (si existe)
2. Ou suivez la doc SendGrid officielle
3. Le code est compatible, changez juste `.env`

---

## ✅ Checklist finale

Avant de lancer votre première campagne :

- [ ] Validation en 2 étapes activée
- [ ] Mot de passe d'application créé
- [ ] `.env` configuré avec `GMAIL_ADDRESS` et `GMAIL_APP_PASSWORD`
- [ ] `python config/settings.py` passe ✅
- [ ] Test d'email envoyé à vous-même réussi
- [ ] `MAX_PROSPECTS_PER_DAY` configuré à 10-20 max
- [ ] Prêt à lancer !

---

**Tout est prêt ! Vous pouvez maintenant lancer votre première campagne avec Gmail !** 🚀

```bash
python scripts/main.py --secteur "coiffeur" --ville "Paris" --limite 10
```
