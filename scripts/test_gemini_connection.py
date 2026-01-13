"""
Script de diagnostic pour tester la connexion à l'API Gemini
Aide à identifier les problèmes de réseau, proxy, ou SSL
"""
import os
import sys
import ssl

# Appliquer les mêmes configurations SSL que le générateur
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '1'
os.environ['GRPC_VERBOSITY'] = 'ERROR'

try:
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    pass

def test_gemini_connection():
    """Test de connexion à l'API Gemini"""
    print("=" * 70)
    print("🔍 DIAGNOSTIC DE CONNEXION GEMINI")
    print("=" * 70)
    print()

    # 1. Vérifier la clé API
    print("1️⃣  Vérification de la clé API...")
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print("❌ GEMINI_API_KEY non définie")
        print("💡 Définissez la variable d'environnement:")
        print("   export GEMINI_API_KEY='votre_clé'")
        print("   ou ajoutez-la dans le fichier .env")
        return False
    else:
        print(f"✓ Clé API trouvée: {api_key[:20]}...{api_key[-10:]}")
    print()

    # 2. Vérifier les variables proxy
    print("2️⃣  Vérification de la configuration proxy...")
    http_proxy = os.getenv('HTTP_PROXY') or os.getenv('http_proxy')
    https_proxy = os.getenv('HTTPS_PROXY') or os.getenv('https_proxy')

    if http_proxy:
        print(f"   HTTP_PROXY: {http_proxy}")
    if https_proxy:
        print(f"   HTTPS_PROXY: {https_proxy}")
    if not http_proxy and not https_proxy:
        print("   Aucun proxy configuré")
    print()

    # 3. Importer le SDK Gemini
    print("3️⃣  Import du SDK Gemini...")
    try:
        import google.generativeai as genai
        print("✓ SDK Gemini importé")
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Installez le SDK: pip install google-generativeai")
        return False
    print()

    # 4. Configurer Gemini
    print("4️⃣  Configuration de Gemini...")
    try:
        genai.configure(api_key=api_key)
        print("✓ Gemini configuré")
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False
    print()

    # 5. Test de connexion simple
    print("5️⃣  Test de connexion (ping simple)...")
    print("   Timeout: 120 secondes")
    print("   Ceci peut prendre du temps avec un proxy...")
    print()

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')  # Flash plus rapide pour le test

        response = model.generate_content(
            "Réponds simplement 'OK'",
            generation_config={'max_output_tokens': 10},
            request_options={'timeout': 120}
        )

        print(f"✓ Connexion réussie!")
        print(f"   Réponse: {response.text}")
        print()
        print("=" * 70)
        print("✅ DIAGNOSTIC COMPLET: SUCCÈS")
        print("=" * 70)
        print()
        print("💡 Vous pouvez maintenant utiliser le générateur de templates:")
        print("   python -m scripts.gemini_template_generator --url URL --theme THEME")
        return True

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Erreur de connexion: {error_msg}")
        print()
        print("=" * 70)
        print("❌ DIAGNOSTIC COMPLET: ÉCHEC")
        print("=" * 70)
        print()
        print("💡 SOLUTIONS POSSIBLES:")
        print()

        # Analyser le type d'erreur
        if "timeout" in error_msg.lower() or "503" in error_msg:
            print("🔧 Problème de timeout/connexion:")
            print("   1. Vérifiez votre connexion internet")
            print("   2. Si vous êtes derrière un proxy d'entreprise:")
            print("      export HTTP_PROXY=http://proxy.entreprise.com:8080")
            print("      export HTTPS_PROXY=http://proxy.entreprise.com:8080")
            print("   3. Vérifiez que le firewall autorise les connexions à:")
            print("      - generativelanguage.googleapis.com")
            print("      - Port 443 (HTTPS)")
            print()

        elif "api key" in error_msg.lower() or "401" in error_msg or "403" in error_msg:
            print("🔧 Problème d'authentification:")
            print("   1. Vérifiez que votre clé API est valide")
            print("   2. Obtenez une clé sur: https://makersuite.google.com/app/apikey")
            print("   3. Assurez-vous qu'elle est active et non expirée")
            print()

        elif "ssl" in error_msg.lower() or "certificate" in error_msg.lower():
            print("🔧 Problème SSL:")
            print("   1. La vérification SSL est déjà désactivée")
            print("   2. Vérifiez votre proxy ne bloque pas les connexions HTTPS")
            print("   3. Contactez votre administrateur réseau")
            print()

        else:
            print("🔧 Erreur inconnue:")
            print("   1. Vérifiez les logs ci-dessus")
            print("   2. Essayez depuis un autre réseau (sans proxy)")
            print("   3. Contactez le support si le problème persiste")
            print()

        print("📝 Pour plus d'aide, consultez:")
        print("   docs/GEMINI_TEMPLATE_GENERATOR.md (section Troubleshooting)")

        return False


if __name__ == "__main__":
    success = test_gemini_connection()
    sys.exit(0 if success else 1)
