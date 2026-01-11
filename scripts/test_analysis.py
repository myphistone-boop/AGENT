"""
Script de test - Analyse de secteur et génération de sites web
Mode TEST sans envoi d'emails, focus sur l'analyse et la génération
"""
import sys
import argparse
from pathlib import Path
from datetime import datetime
import json

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.modules.google_maps_scraper import GoogleMapsScraper
from scripts.modules.website_scraper import WebsiteScraper
from scripts.modules.website_analyzer import WebsiteAnalyzer
from scripts.modules.color_extractor import ColorExtractor
from scripts.modules.content_generator import ContentGenerator
from scripts.modules.html_generator import HTMLGenerator
from scripts.modules.screenshot_maker import ScreenshotMaker
from scripts.utils.logger import setup_logger
from scripts.utils.file_manager import FileManager
from config import settings

logger = setup_logger("test_analysis")


class SectorAnalyzer:
    """Analyseur de secteur - Mode test pour évaluer et générer des sites"""

    def __init__(self):
        self.file_manager = FileManager()
        self.color_extractor = ColorExtractor()
        self.content_generator = ContentGenerator()
        self.html_generator = HTMLGenerator()
        self.screenshot_maker = ScreenshotMaker()
        self.website_analyzer = WebsiteAnalyzer()

        # Stats
        self.stats = {
            'total_found': 0,
            'with_website': 0,
            'without_website': 0,
            'outdated_sites': 0,
            'modern_sites': 0,
            'generated': 0,
            'errors': 0
        }

        # Résultats détaillés
        self.results = []

    def analyze_sector(self, sector, city, max_prospects=5):
        """
        Analyse un secteur complet

        Args:
            sector: Secteur d'activité (ex: "coiffeur")
            city: Ville
            max_prospects: Nombre max de prospects à analyser
        """
        logger.info(f"{'='*70}")
        logger.info(f"🔍 ANALYSE DE SECTEUR - MODE TEST")
        logger.info(f"{'='*70}")
        logger.info(f"Secteur: {sector}")
        logger.info(f"Ville: {city}")
        logger.info(f"Limite: {max_prospects} prospects")
        logger.info(f"{'='*70}\n")

        # 1. SCRAPING GOOGLE MAPS
        logger.info("📍 ÉTAPE 1/3 : Recherche sur Google Maps")
        logger.info("="*70)

        prospects = self._scrape_google_maps(sector, city, max_prospects)

        if not prospects:
            logger.error("❌ Aucun prospect trouvé")
            return False

        # 2. ANALYSE ET GÉNÉRATION
        logger.info(f"\n🔄 ÉTAPE 2/3 : Analyse et génération ({len(prospects)} prospects)")
        logger.info("="*70)

        for idx, prospect in enumerate(prospects, 1):
            logger.info(f"\n{'─'*70}")
            logger.info(f"Prospect {idx}/{len(prospects)}: {prospect['name']}")
            logger.info(f"{'─'*70}")

            try:
                result = self._analyze_and_generate(prospect, idx)
                if result:
                    self.results.append(result)
                    self.stats['generated'] += 1

            except Exception as e:
                logger.error(f"❌ Erreur: {str(e)}")
                self.stats['errors'] += 1
                continue

        # 3. RAPPORT FINAL
        logger.info(f"\n📊 ÉTAPE 3/3 : Génération du rapport d'analyse")
        logger.info("="*70)

        self._generate_report(sector, city)

        logger.info(f"\n{'='*70}")
        logger.info(f"✅ ANALYSE TERMINÉE")
        logger.info(f"{'='*70}\n")

        return True

    def _scrape_google_maps(self, sector, city, max_results):
        """Scrape Google Maps pour trouver des prospects"""
        logger.info(f"🔍 Recherche: {sector} à {city}")

        maps_scraper = GoogleMapsScraper(headless=True)

        try:
            prospects = maps_scraper.search(sector, city, max_results)
            self.stats['total_found'] = len(prospects)

            # Compter avec/sans site
            for p in prospects:
                if p.get('website'):
                    self.stats['with_website'] += 1
                else:
                    self.stats['without_website'] += 1

            logger.info(f"\n📊 Trouvés:")
            logger.info(f"   Total: {len(prospects)}")
            logger.info(f"   Avec site web: {self.stats['with_website']}")
            logger.info(f"   Sans site web: {self.stats['without_website']}")

            return prospects

        finally:
            maps_scraper.close()

    def _analyze_and_generate(self, prospect, prospect_id):
        """
        Analyse un site existant et génère une version améliorée

        Args:
            prospect: Données du prospect (Google Maps)
            prospect_id: ID numérique du prospect

        Returns:
            dict: Résultat de l'analyse
        """
        client_id = f"test_{prospect_id:03d}"
        has_website = bool(prospect.get('website'))

        logger.info(f"Type: {'AVEC site web' if has_website else 'SANS site web'}")
        logger.info(f"URL: {prospect.get('website', 'N/A')}")
        logger.info(f"Catégorie: {prospect.get('category', 'N/A')}")

        # Données business
        business_data = {
            'id': client_id,
            'name': prospect['name'],
            'address': prospect.get('address', ''),
            'phone': prospect.get('phone', ''),
            'rating': prospect.get('rating'),
            'reviews_count': prospect.get('reviews_count'),
            'category': prospect.get('category', '')
        }

        # Déterminer le secteur
        sector = self._detect_sector(prospect.get('category', ''))
        logger.info(f"Secteur détecté: {sector}")

        result = {
            'prospect_id': prospect_id,
            'name': prospect['name'],
            'has_website': has_website,
            'website_url': prospect.get('website'),
            'category': prospect.get('category'),
            'sector': sector,
            'timestamp': datetime.now().isoformat()
        }

        if has_website:
            # ANALYSE DU SITE EXISTANT
            result.update(self._analyze_existing_website(
                prospect, client_id, sector, business_data
            ))
        else:
            # GÉNÉRATION DEPUIS ZÉRO
            result.update(self._generate_new_website(
                prospect, client_id, sector, business_data
            ))

        return result

    def _analyze_existing_website(self, prospect, client_id, sector, business_data):
        """Analyse un site web existant"""
        logger.info("\n🌐 Scraping et analyse du site...")

        # 1. Scraper le site
        web_scraper = WebsiteScraper(client_id, prospect['website'])
        site_data = web_scraper.scrape()

        if not site_data:
            logger.warning("⚠️  Échec du scraping")
            return {'error': 'Scraping failed', 'analysis': None}

        # 2. Analyser la qualité du site
        logger.info("🔍 Analyse de la qualité...")

        # Récupérer le HTML pour l'analyse
        html_content = ""
        try:
            import requests
            response = requests.get(
                prospect['website'],
                timeout=10,
                verify=settings.VERIFY_SSL,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            html_content = response.text
        except:
            logger.warning("⚠️  Impossible de récupérer le HTML pour analyse approfondie")

        analysis = self.website_analyzer.analyze(html_content, site_data)

        # Mettre à jour les stats
        if analysis['is_outdated']:
            self.stats['outdated_sites'] += 1
        else:
            self.stats['modern_sites'] += 1

        # 3. Extraire les couleurs
        colors = None
        if site_data.get('logo'):
            logger.info("🎨 Extraction couleurs du logo...")
            colors = self.color_extractor.extract_from_logo(site_data['logo'])

        if not colors:
            colors = self.color_extractor.get_default_palette(sector)

        # 4. Générer une version améliorée
        logger.info("✨ Génération d'une version améliorée...")

        template_data = {
            'name': business_data['name'],
            'hero_title': site_data.get('title', business_data['name']),
            'hero_subtitle': site_data.get('description', ''),
            'phone': business_data['phone'] or site_data.get('phone', ''),
            'email': site_data.get('email', ''),
            'address': business_data['address'],
            'logo': site_data.get('logo'),
            'images': site_data.get('images', []),
            'texts': site_data.get('texts', []),
            'cta': 'Nous contacter'
        }

        html_path = self.html_generator.generate(client_id, sector, template_data, colors)

        if not html_path:
            return {'error': 'HTML generation failed', 'analysis': analysis}

        # 5. Capturer les screenshots
        logger.info("📸 Capture screenshots (avant/après)...")
        screenshots = self.screenshot_maker.capture_website(html_path, client_id, "generated")

        # Afficher les résultats de l'analyse
        logger.info(f"\n{'─'*70}")
        logger.info(f"📊 RÉSULTATS D'ANALYSE:")
        logger.info(f"{'─'*70}")
        logger.info(f"Score: {analysis['score']}/100")
        logger.info(f"Qualité: {analysis['quality']}")
        logger.info(f"Site daté: {'OUI ⚠️' if analysis['is_outdated'] else 'NON ✅'}")
        logger.info(f"Recommandation: {analysis['recommendation']}")

        if analysis['strengths']:
            logger.info(f"\n✅ Points forts:")
            for strength in analysis['strengths'][:5]:
                logger.info(f"   • {strength}")

        if analysis['issues']:
            logger.info(f"\n⚠️  Problèmes ({len(analysis['issues'])}):")
            for issue in analysis['issues'][:5]:
                logger.info(f"   • {issue}")

        logger.info(f"\n📁 Fichiers générés:")
        logger.info(f"   HTML: {html_path}")
        logger.info(f"   Screenshot original: {site_data.get('screenshot_original', 'N/A')}")
        logger.info(f"   Screenshot nouveau: {screenshots.get('desktop', 'N/A')}")

        return {
            'analysis': analysis,
            'site_data': {
                'title': site_data.get('title'),
                'description': site_data.get('description'),
                'phone': site_data.get('phone'),
                'email': site_data.get('email'),
                'has_logo': bool(site_data.get('logo')),
                'images_count': len(site_data.get('images', [])),
                'texts_count': len(site_data.get('texts', []))
            },
            'generated_html': str(html_path),
            'screenshots': screenshots,
            'colors': colors,
            'error': None
        }

    def _generate_new_website(self, prospect, client_id, sector, business_data):
        """Génère un nouveau site web depuis zéro"""
        logger.info("\n🤖 Génération d'un nouveau site web...")

        # 1. Générer le contenu avec IA (si activé)
        if settings.USE_AI_FOR_NO_SITE and settings.ANTHROPIC_API_KEY:
            logger.info("🤖 Génération contenu IA...")
            ai_content = self.content_generator.generate_website_content(
                business_data['name'],
                business_data['category'],
                business_data['address'].split(',')[-1].strip()
            )
        else:
            logger.info("ℹ️  Contenu par défaut (IA désactivée)")
            ai_content = {
                'hero_subtitle': f"Votre {business_data['category']} de confiance",
                'slogan': f"Bienvenue chez {business_data['name']}",
                'services': ['Service 1', 'Service 2', 'Service 3'],
                'about': f"{business_data['name']} est à votre service.",
                'cta': 'Nous contacter'
            }

        # 2. Couleurs par défaut
        colors = self.color_extractor.get_default_palette(sector)

        # 3. Générer HTML
        template_data = {
            'name': business_data['name'],
            'hero_title': business_data['name'],
            'hero_subtitle': ai_content.get('hero_subtitle', ''),
            'slogan': ai_content.get('slogan', ''),
            'phone': business_data['phone'],
            'address': business_data['address'],
            'services': ai_content.get('services', []),
            'about': ai_content.get('about', ''),
            'cta': ai_content.get('cta', 'Nous contacter')
        }

        logger.info("🎨 Génération HTML...")
        html_path = self.html_generator.generate(client_id, sector, template_data, colors)

        if not html_path:
            return {'error': 'HTML generation failed'}

        # 4. Screenshots
        logger.info("📸 Capture screenshots...")
        screenshots = self.screenshot_maker.capture_website(html_path, client_id, "generated")

        logger.info(f"\n📁 Fichiers générés:")
        logger.info(f"   HTML: {html_path}")
        logger.info(f"   Screenshot: {screenshots.get('desktop', 'N/A')}")

        return {
            'analysis': None,
            'ai_content': ai_content,
            'generated_html': str(html_path),
            'screenshots': screenshots,
            'colors': colors,
            'error': None
        }

    def _detect_sector(self, category):
        """Détecte le secteur depuis la catégorie Google Maps"""
        category_lower = category.lower()

        if 'coif' in category_lower or 'salon' in category_lower or 'beauté' in category_lower or 'esthét' in category_lower:
            return 'beaute'
        elif 'plomb' in category_lower or 'électric' in category_lower or 'menuiserie' in category_lower or 'artisan' in category_lower:
            return 'artisan'
        elif 'restaurant' in category_lower or 'café' in category_lower or 'boulangerie' in category_lower or 'pizzeria' in category_lower:
            return 'restauration'
        elif 'médecin' in category_lower or 'dentist' in category_lower or 'kiné' in category_lower or 'cabinet' in category_lower:
            return 'sante'
        elif any(word in category_lower for word in ['thérapeu', 'naturo', 'ostéo', 'acupun', 'massage', 'reiki', 'énergé', 'chiropra', 'psychothéra', 'hypnothéra', 'réflexo', 'médecine douce', 'holistique']):
            return 'therapeute'
        else:
            return 'commerce'

    def _generate_report(self, sector, city):
        """Génère un rapport d'analyse détaillé"""
        report_path = self.file_manager.get_output_path(
            'report',
            f"analyse_{sector}_{city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        # Rapport texte
        report_text = f"""
{'='*70}
RAPPORT D'ANALYSE DE SECTEUR
{'='*70}

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Secteur: {sector}
Ville: {city}

{'='*70}
STATISTIQUES GLOBALES
{'='*70}

Prospects trouvés:        {self.stats['total_found']}
  - Avec site web:        {self.stats['with_website']}
  - Sans site web:        {self.stats['without_website']}

Analyse des sites:
  - Sites modernes:       {self.stats['modern_sites']}
  - Sites datés:          {self.stats['outdated_sites']}

Sites générés:            {self.stats['generated']}
Erreurs:                  {self.stats['errors']}

{'='*70}
RÉSULTATS DÉTAILLÉS
{'='*70}
"""

        for idx, result in enumerate(self.results, 1):
            report_text += f"\n{idx}. {result['name']}\n"
            report_text += f"   Catégorie: {result['category']}\n"
            report_text += f"   Secteur: {result['sector']}\n"

            if result['has_website']:
                report_text += f"   URL: {result['website_url']}\n"

                if result.get('analysis'):
                    analysis = result['analysis']
                    report_text += f"   Score qualité: {analysis['score']}/100\n"
                    report_text += f"   État: {analysis['quality']}\n"
                    report_text += f"   Daté: {'OUI' if analysis['is_outdated'] else 'NON'}\n"
                    report_text += f"   Recommandation: {analysis['recommendation']}\n"

                    if analysis['issues']:
                        report_text += f"   Problèmes: {len(analysis['issues'])} détectés\n"
            else:
                report_text += f"   Pas de site web - Généré depuis zéro\n"

            if result.get('generated_html'):
                report_text += f"   HTML généré: {result['generated_html']}\n"

            report_text += "\n"

        report_text += f"""
{'='*70}
CONCLUSION
{'='*70}

Taux de sites datés: {(self.stats['outdated_sites'] / self.stats['with_website'] * 100) if self.stats['with_website'] > 0 else 0:.1f}%
Opportunités détectées: {self.stats['outdated_sites']} sites nécessitant une refonte

Fichiers générés disponibles dans: outputs/

{'='*70}
"""

        # Sauvegarder le rapport texte
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)

        logger.info(report_text)
        logger.info(f"💾 Rapport sauvegardé: {report_path}")

        # Sauvegarder aussi en JSON pour analyse ultérieure
        json_path = report_path.replace('.txt', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'sector': sector,
                'city': city,
                'timestamp': datetime.now().isoformat(),
                'stats': self.stats,
                'results': self.results
            }, f, ensure_ascii=False, indent=2)

        logger.info(f"💾 Données JSON: {json_path}")


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description='Analyseur de secteur - Test sans prospection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Analyser 5 coiffeurs à Paris
  python test_analysis.py --secteur "coiffeur" --ville "Paris" --limite 5

  # Analyser 3 restaurants à Lyon
  python test_analysis.py --secteur "restaurant" --ville "Lyon" --limite 3

  # Analyser 10 plombiers à Marseille
  python test_analysis.py --secteur "plombier" --ville "Marseille" --limite 10

Ce script va:
  1. Chercher des établissements sur Google Maps
  2. Analyser leur site web existant (qualité, modernité)
  3. Générer une version améliorée
  4. Créer des screenshots avant/après
  5. Produire un rapport d'analyse détaillé

AUCUN EMAIL N'EST ENVOYÉ - Mode test uniquement
        """
    )

    parser.add_argument('--secteur', type=str, required=True, help='Secteur activité (ex: coiffeur, restaurant, plombier)')
    parser.add_argument('--ville', type=str, required=True, help='Ville')
    parser.add_argument('--limite', type=int, default=5, help='Nombre max de prospects à analyser (défaut: 5)')

    args = parser.parse_args()

    # Créer l'analyseur
    analyzer = SectorAnalyzer()

    # Lancer l'analyse
    analyzer.analyze_sector(args.secteur, args.ville, args.limite)


if __name__ == "__main__":
    main()
