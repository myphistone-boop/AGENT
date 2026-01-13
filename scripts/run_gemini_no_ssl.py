"""
Wrapper pour exécuter le générateur Gemini sans vérification SSL
À utiliser si vous avez des problèmes de certificats (proxy d'entreprise, etc.)
"""
import os
import sys

# Désactiver la vérification SSL pour gRPC (utilisé par Gemini)
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '1'
os.environ['GRPC_VERBOSITY'] = 'ERROR'  # Réduire les logs gRPC

# Forcer l'utilisation de certificats système ou désactiver la vérification
try:
    import ssl
    # Créer un contexte SSL qui n'a pas besoin de vérification
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass

# Maintenant importer et exécuter le générateur
from scripts.gemini_template_generator import main

if __name__ == "__main__":
    print("⚠️  MODE SANS VÉRIFICATION SSL (pour proxy d'entreprise)")
    print("=" * 60)
    main()
