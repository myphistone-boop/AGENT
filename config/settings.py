"""
Configuration centrale du projet
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# ===== CHEMINS =====
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_PATH = BASE_DIR / "templates"
OUTPUT_PATH = BASE_DIR / "outputs"
TEMP_PATH = BASE_DIR / "temp"
DATA_PATH = BASE_DIR / "data"

# ===== CONFIGURATION EMAIL =====
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY', '')
FROM_EMAIL = os.getenv('FROM_EMAIL', '')
FROM_NAME = os.getenv('FROM_NAME', '')

# ===== CONFIGURATION IA =====
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
USE_AI_FOR_NO_SITE = os.getenv('USE_AI_FOR_NO_SITE', 'true').lower() == 'true'

# ===== PARAMÈTRES PROSPECTION =====
MAX_PROSPECTS_PER_DAY = int(os.getenv('MAX_PROSPECTS_PER_DAY', 50))
DELAY_BETWEEN_EMAILS = int(os.getenv('DELAY_BETWEEN_EMAILS', 2))

# ===== PROXY ET SSL =====
HTTP_PROXY = os.getenv('HTTP_PROXY', '')
HTTPS_PROXY = os.getenv('HTTPS_PROXY', '')
VERIFY_SSL = os.getenv('VERIFY_SSL', 'true').lower() == 'true'

PROXIES = {}
if HTTP_PROXY:
    PROXIES['http'] = HTTP_PROXY
if HTTPS_PROXY:
    PROXIES['https'] = HTTPS_PROXY

# ===== DEBUG =====
DEBUG_MODE = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# ===== COULEURS PAR DÉFAUT PAR SECTEUR =====
DEFAULT_COLORS = {
    'beaute': {
        'primary': '#e91e63',
        'secondary': '#9c27b0',
        'accent': '#f8bbd0'
    },
    'artisan': {
        'primary': '#2196f3',
        'secondary': '#1976d2',
        'accent': '#64b5f6'
    },
    'restauration': {
        'primary': '#ff5722',
        'secondary': '#795548',
        'accent': '#ffccbc'
    },
    'sante': {
        'primary': '#4caf50',
        'secondary': '#388e3c',
        'accent': '#c8e6c9'
    },
    'commerce': {
        'primary': '#ff9800',
        'secondary': '#f57c00',
        'accent': '#ffe0b2'
    }
}

# ===== MAPPING TYPES GOOGLE MAPS → SECTEURS =====
SECTOR_MAPPING = {
    # Beauté
    'hair_care': 'beaute',
    'beauty_salon': 'beaute',
    'spa': 'beaute',
    'nail_salon': 'beaute',

    # Artisan
    'plumber': 'artisan',
    'electrician': 'artisan',
    'carpenter': 'artisan',
    'painter': 'artisan',
    'locksmith': 'artisan',
    'general_contractor': 'artisan',

    # Restauration
    'restaurant': 'restauration',
    'cafe': 'restauration',
    'bakery': 'restauration',
    'bar': 'restauration',
    'meal_delivery': 'restauration',
    'meal_takeaway': 'restauration',

    # Santé
    'physiotherapist': 'sante',
    'doctor': 'sante',
    'dentist': 'sante',
    'pharmacy': 'sante',
    'hospital': 'sante',

    # Commerce
    'store': 'commerce',
    'clothing_store': 'commerce',
    'shoe_store': 'commerce',
    'jewelry_store': 'commerce',
    'book_store': 'commerce',
    'electronics_store': 'commerce'
}

# ===== VALIDATION =====
def validate_config():
    """Valide que la configuration minimale est présente"""
    errors = []

    if not SENDGRID_API_KEY:
        errors.append("❌ SENDGRID_API_KEY manquante dans .env")

    if not FROM_EMAIL:
        errors.append("❌ FROM_EMAIL manquante dans .env")

    if not FROM_NAME:
        errors.append("❌ FROM_NAME manquant dans .env")

    if USE_AI_FOR_NO_SITE and not ANTHROPIC_API_KEY:
        errors.append("⚠️  ANTHROPIC_API_KEY manquante (nécessaire si USE_AI_FOR_NO_SITE=true)")

    return errors

if __name__ == "__main__":
    # Test de la configuration
    print("🔍 Validation de la configuration...")
    errors = validate_config()

    if errors:
        print("\n".join(errors))
    else:
        print("✅ Configuration valide !")
        print(f"📧 Email: {FROM_EMAIL}")
        print(f"🎯 Max prospects/jour: {MAX_PROSPECTS_PER_DAY}")
        print(f"🤖 IA activée: {USE_AI_FOR_NO_SITE}")
        print(f"🌐 Proxy configuré: {'Oui' if PROXIES else 'Non'}")
        print(f"🔒 SSL vérifié: {VERIFY_SSL}")
