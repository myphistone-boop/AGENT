"""
Test rapide - Vérification que le système d'analyse fonctionne
"""
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.utils.logger import setup_logger
from config import settings

logger = setup_logger("quick_test")


def test_configuration():
    """Teste la configuration de base"""
    logger.info("="*70)
    logger.info("🔍 TEST DE CONFIGURATION")
    logger.info("="*70)

    # Vérifier les modules
    try:
        from scripts.modules.google_maps_scraper import GoogleMapsScraper
        from scripts.modules.website_scraper import WebsiteScraper
        from scripts.modules.website_analyzer import WebsiteAnalyzer
        from scripts.modules.color_extractor import ColorExtractor
        from scripts.modules.html_generator import HTMLGenerator
        from scripts.modules.screenshot_maker import ScreenshotMaker
        logger.info("✅ Tous les modules sont importables")
    except ImportError as e:
        logger.error(f"❌ Erreur d'import: {e}")
        return False

    # Vérifier la config
    logger.info("\n📋 Configuration détectée:")
    logger.info(f"   HTTP_PROXY: {'✅ Configuré' if settings.HTTP_PROXY else '⚪ Non configuré'}")
    logger.info(f"   HTTPS_PROXY: {'✅ Configuré' if settings.HTTPS_PROXY else '⚪ Non configuré'}")
    logger.info(f"   VERIFY_SSL: {settings.VERIFY_SSL}")
    logger.info(f"   ANTHROPIC_API_KEY: {'✅ Configuré' if settings.ANTHROPIC_API_KEY else '⚪ Non configuré (optionnel pour test)'}")
    logger.info(f"   USE_AI_FOR_NO_SITE: {settings.USE_AI_FOR_NO_SITE}")

    # Vérifier les templates
    templates_dir = Path("templates")
    if templates_dir.exists():
        sectors = [d.name for d in templates_dir.iterdir() if d.is_dir()]
        logger.info(f"\n📁 Templates disponibles: {', '.join(sectors)}")
        logger.info("✅ Templates trouvés")
    else:
        logger.error("❌ Dossier templates introuvable")
        return False

    # Vérifier Playwright
    logger.info("\n🌐 Test Playwright...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        logger.info("✅ Playwright fonctionne")
    except Exception as e:
        logger.error(f"❌ Playwright non installé ou erreur: {e}")
        logger.info("   Installez avec: playwright install chromium")
        return False

    logger.info("\n" + "="*70)
    logger.info("✅ CONFIGURATION OK - Prêt pour les tests")
    logger.info("="*70)

    return True


def test_analyzer():
    """Teste l'analyseur de sites web"""
    logger.info("\n" + "="*70)
    logger.info("🔍 TEST DE L'ANALYSEUR DE SITES")
    logger.info("="*70)

    from scripts.modules.website_analyzer import WebsiteAnalyzer

    # HTML de test (site obsolète)
    html_obsolete = """
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body>
        <table width="100%" height="100%">
            <tr><td>Contenu en table</td></tr>
        </table>
    </body>
    </html>
    """

    analyzer = WebsiteAnalyzer()
    report = analyzer.analyze(html_obsolete, {})

    logger.info(f"\nTest HTML obsolète (tables):")
    logger.info(f"   Score: {report['score']}/100")
    logger.info(f"   Qualité: {report['quality']}")
    logger.info(f"   Daté: {'OUI' if report['is_outdated'] else 'NON'}")

    # HTML de test (site moderne)
    html_modern = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            .hero {
                display: flex;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            @media (max-width: 768px) { .hero { flex-direction: column; } }
        </style>
    </head>
    <body>
        <header><nav><a href="#">Menu</a></nav></header>
        <main>
            <section class="hero"><h1>Titre</h1></section>
        </main>
        <footer>Footer</footer>
    </body>
    </html>
    """

    report = analyzer.analyze(html_modern, {'logo': 'logo.png', 'images': ['1.jpg', '2.jpg']})

    logger.info(f"\nTest HTML moderne (HTML5, flexbox, gradients):")
    logger.info(f"   Score: {report['score']}/100")
    logger.info(f"   Qualité: {report['quality']}")
    logger.info(f"   Daté: {'OUI' if report['is_outdated'] else 'NON'}")

    logger.info("\n✅ Analyseur testé avec succès")

    return True


def test_html_generation():
    """Teste la génération HTML"""
    logger.info("\n" + "="*70)
    logger.info("🎨 TEST DE GÉNÉRATION HTML")
    logger.info("="*70)

    from scripts.modules.html_generator import HTMLGenerator
    from scripts.modules.color_extractor import ColorExtractor

    html_gen = HTMLGenerator()
    color_ext = ColorExtractor()

    # Données de test
    template_data = {
        'name': 'Salon Test',
        'hero_title': 'Bienvenue chez Salon Test',
        'hero_subtitle': 'Votre salon de beauté à Paris',
        'phone': '01 23 45 67 89',
        'address': '123 Rue de Test, 75001 Paris',
        'cta': 'Prendre rendez-vous'
    }

    colors = color_ext.get_default_palette('beaute')

    logger.info(f"Génération pour secteur: beaute")
    logger.info(f"Palette: {colors}")

    try:
        html_path = html_gen.generate('test_quick', 'beaute', template_data, colors)

        if html_path and Path(html_path).exists():
            logger.info(f"✅ HTML généré: {html_path}")

            # Vérifier le contenu
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()

            checks = [
                ('Salon Test' in content, 'Nom du salon'),
                ('Bienvenue' in content, 'Titre hero'),
                ('01 23 45 67 89' in content, 'Téléphone'),
                ('linear-gradient' in content, 'Dégradés CSS'),
                ('@media' in content, 'Media queries'),
            ]

            logger.info("\nVérifications:")
            for check, name in checks:
                logger.info(f"   {'✅' if check else '❌'} {name}")

            return all(check for check, _ in checks)
        else:
            logger.error("❌ Échec génération HTML")
            return False

    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        return False


def main():
    """Lancer tous les tests"""
    logger.info("\n" + "="*70)
    logger.info("🚀 TEST RAPIDE DU SYSTÈME D'ANALYSE")
    logger.info("="*70)

    tests = [
        ("Configuration", test_configuration),
        ("Analyseur de sites", test_analyzer),
        ("Génération HTML", test_html_generation),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            logger.error(f"❌ Erreur dans {name}: {e}")
            results.append((name, False))

    # Rapport final
    logger.info("\n" + "="*70)
    logger.info("📊 RÉSUMÉ DES TESTS")
    logger.info("="*70)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {name}")

    all_passed = all(result for _, result in results)

    if all_passed:
        logger.info("\n" + "="*70)
        logger.info("🎉 TOUS LES TESTS SONT PASSÉS !")
        logger.info("="*70)
        logger.info("\nVous pouvez maintenant lancer une analyse complète:")
        logger.info('   python scripts/test_analysis.py --secteur "coiffeur" --ville "Paris" --limite 3')
        logger.info("\nOu tester le pipeline complet (avec emails):")
        logger.info('   python scripts/main.py --secteur "coiffeur" --ville "Paris" --limite 5')
    else:
        logger.error("\n" + "="*70)
        logger.error("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        logger.error("="*70)
        logger.error("\nVérifiez les erreurs ci-dessus et:")
        logger.error("   1. Installez les dépendances: pip install -r requirements.txt")
        logger.error("   2. Installez Playwright: playwright install chromium")
        logger.error("   3. Vérifiez votre configuration .env")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
