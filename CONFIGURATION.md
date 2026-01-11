# 🔧 Configuration Détaillée

## ✅ Ce qui est OBLIGATOIRE

### 1. SendGrid (pour les emails)

**Étapes :**
1. Allez sur https://sendgrid.com
2. Créez un compte gratuit
3. Settings → API Keys → Create API Key
4. Choisissez "Full Access"
5. Copiez la clé (format : `SG.xxxxxxx...`)

**Dans le fichier `.env` :**
```env
SENDGRID_API_KEY=SG.votre_cle_complete_ici
FROM_EMAIL=vous@votredomaine.com
FROM_NAME=Votre Nom
```

**⚠️ IMPORTANT :** N'utilisez PAS @gmail.com pour FROM_EMAIL. Utilisez un domaine professionnel.

---

### 2. Configuration DNS (pour éviter les spams)

**Si vous avez votre propre domaine :**

1. Dans SendGrid, allez dans Settings → Sender Authentication
2. Cliquez "Authenticate Your Domain"
3. Entrez votre domaine (ex: votreentreprise.com)
4. SendGrid vous donnera des records DNS à ajouter

**Ajoutez ces records chez votre registrar (OVH, Gandi, etc.) :**
- Type CNAME pour DKIM
- Type TXT pour SPF

**Pourquoi ?** Sans ça, vos emails arrivent en spam.

---

## 🟡 Ce qui est OPTIONNEL mais recommandé

### 3. Claude AI (pour clients sans site)

**Si vous voulez utiliser l'IA pour générer du contenu :**

1. Allez sur https://console.anthropic.com
2. Créez un compte
3. Settings → API Keys → Create Key
4. Ajoutez $5-10 de crédits (coût : ~$0.03 par client sans site)

**Dans `.env` :**
```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxx
USE_AI_FOR_NO_SITE=true
```

**Si vous ne voulez PAS l'IA :**
```env
USE_AI_FOR_NO_SITE=false
```

Dans ce cas, seuls les clients qui ont DÉJÀ un site seront contactés.

---

## 🌐 Configuration Proxy (si PC entreprise)

**Si vous êtes sur un PC d'entreprise avec firewall/proxy :**

### Trouver votre proxy

**Windows :**
1. Paramètres → Réseau et Internet → Proxy
2. Notez l'adresse et le port

**Mac/Linux :**
```bash
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

**Dans `.env` :**
```env
HTTP_PROXY=http://proxy.entreprise.com:8080
HTTPS_PROXY=http://proxy.entreprise.com:8080
```

---

## 🔒 Configuration SSL

**Si vous avez des erreurs SSL :**

Essayez d'abord SANS désactiver SSL. Seulement en dernier recours :

```env
VERIFY_SSL=false
```

⚠️ **Attention :** Ceci désactive la vérification des certificats (moins sécurisé).

---

## 🎯 Paramètres de prospection

```env
MAX_PROSPECTS_PER_DAY=50
DELAY_BETWEEN_EMAILS=2
```

**Explications :**
- `MAX_PROSPECTS_PER_DAY` : Limite de sécurité (ne pas dépasser 50/jour au début)
- `DELAY_BETWEEN_EMAILS` : Délai en secondes entre chaque email (évite rate limiting)

---

## 📝 Votre fichier .env complet

Voici un exemple de fichier `.env` correctement configuré :

```env
# ========== OBLIGATOIRE ==========
SENDGRID_API_KEY=SG.abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
FROM_EMAIL=contact@monentreprise.com
FROM_NAME=Jean Dupont

# ========== OPTIONNEL - IA ==========
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
USE_AI_FOR_NO_SITE=true

# ========== OPTIONNEL - Proxy (si PC entreprise) ==========
HTTP_PROXY=
HTTPS_PROXY=
# Exemple si besoin : HTTP_PROXY=http://proxy.entreprise.com:8080

# ========== OPTIONNEL - SSL (si erreurs) ==========
VERIFY_SSL=true
# Mettre à false SEULEMENT si erreurs SSL persistantes

# ========== PARAMÈTRES ==========
MAX_PROSPECTS_PER_DAY=50
DELAY_BETWEEN_EMAILS=2
DEBUG_MODE=false
LOG_LEVEL=INFO
```

---

## ✅ Vérifier la configuration

**Après avoir créé votre `.env`, testez :**

```bash
python config/settings.py
```

**Vous devez voir :**
```
🔍 Validation de la configuration...
✅ Configuration valide !
📧 Email: contact@monentreprise.com
🎯 Max prospects/jour: 50
🤖 IA activée: True
🌐 Proxy configuré: Non
🔒 SSL vérifié: True
```

**Si vous voyez des ❌**, corrigez avant de continuer !

---

## 🚨 Erreurs courantes

### "SENDGRID_API_KEY manquante dans .env"

➡️ Vous n'avez pas créé le fichier `.env` ou il est vide

**Solution :**
```bash
cp .env.example .env
nano .env  # ou votre éditeur
```

### "FROM_EMAIL manquante dans .env"

➡️ Vous avez oublié de remplir FROM_EMAIL

**Solution :** Ajoutez une ligne dans `.env` :
```env
FROM_EMAIL=votre-email@votredomaine.com
```

### "ANTHROPIC_API_KEY manquante (nécessaire si USE_AI_FOR_NO_SITE=true)"

➡️ Soit vous ajoutez la clé Claude, soit vous désactivez l'IA

**Solution 1 - Ajouter la clé :**
```env
ANTHROPIC_API_KEY=sk-ant-votre-cle
```

**Solution 2 - Désactiver l'IA :**
```env
USE_AI_FOR_NO_SITE=false
```

---

## 🎓 Tutoriel vidéo (si vous bloquez)

### SendGrid

1. https://www.youtube.com/results?search_query=sendgrid+api+key+tutorial
2. Cherchez "How to get SendGrid API key"

### DNS Authentication

1. https://docs.sendgrid.com/ui/account-and-settings/how-to-set-up-domain-authentication
2. Suivez le guide SendGrid (très bien fait)

---

## 📞 Besoin d'aide ?

1. ✅ Vérifiez cette page en premier
2. ✅ Lisez `TROUBLESHOOTING.md` (si existe)
3. ✅ Testez module par module avec `python scripts/modules/nom_module.py --help`

---

**Une fois configuré, vous n'aurez plus JAMAIS à retoucher à ces fichiers !** 🎉
