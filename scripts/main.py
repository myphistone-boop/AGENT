"""
Script principal - Orchestrateur du système
Permet de lancer l'intégralité du process ou des segments individuels
"""
import sys
import argparse
from pathlib import Path
from datetime import datetime
import csv

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts.modules.google_maps_scraper import GoogleMapsScraper
from scripts.modules.website_scraper import WebsiteScraper
from scripts.modules.color_extractor import ColorExtractor
from scripts.modules.content_generator import ContentGenerator
from scripts.modules.html_generator import HTMLGenerator
from scripts.modules.screenshot_maker import ScreenshotMaker
from scripts.modules.pdf_generator import PDFGenerator
from scripts.modules.email_sender import EmailSender
from scripts.utils.logger import setup_logger
from scripts.utils.file_manager import FileManager
from config import settings

logger = setup_logger("main")


class ProspectAgent:
    """Agent principal de prospection automatisée"""

    def __init__(self):
        self.file_manager = FileManager()

        # Initialiser tous les modules
        self.maps_scraper = None
        self.color_extractor = ColorExtractor()
        self.content_generator = ContentGenerator()
        self.html_generator = HTMLGenerator()
        self.screenshot_maker = ScreenshotMaker()
        self.pdf_generator = PDFGenerator()
        self.email_sender = EmailSender()

        # Stats
        self.stats = {
            'total': 0,
            'with_website': 0,
            'without_website': 0,
            'emails_sent': 0,
            'errors': 0
        }

    def run_full_pipeline(self, sector, city, max_prospects=50):
        """
        Lance le pipeline complet

        Args:
            sector: Secteur d'activité (ex: "coiffeur")
            city: Ville
            max_prospects: Nombre max de prospects
        """
        logger.info(f"{'='*60}")
        logger.info(f"🚀 DÉMARRAGE DU PIPELINE COMPLET")
        logger.info(f"{'='*60}")
        logger.info(f"Secteur: {sector}")
        logger.info(f"Ville: {city}")
        logger.info(f"Max prospects: {max_prospects}")
        logger.info(f"{'='*60}\n")

        # Validation config
        errors = settings.validate_config()
        if errors:
            logger.error("❌ Configuration invalide:")
            for error in errors:
                logger.error(f"   {error}")
            return False

        # 1. SCRAPING GOOGLE MAPS
        logger.info("\n📍 ÉTAPE 1/5 : Scraping Google Maps")
        logger.info("="*60)

        prospects = self.scrape_google_maps(sector, city, max_prospects)

        if not prospects:
            logger.error("❌ Aucun prospect trouvé")
            return False

        # Sauvegarder la liste
        prospects_file = self.file_manager.get_prospects_file()
        self._save_prospects_csv(prospects, prospects_file)

        # 2. TRAITEMENT INDIVIDUEL
        logger.info(f"\n🔄 ÉTAPE 2/5 : Traitement des {len(prospects)} prospects")
        logger.info("="*60)

        for idx, prospect in enumerate(prospects, 1):
            logger.info(f"\n--- Prospect {idx}/{len(prospects)} : {prospect['name']} ---")

            try:
                self.process_prospect(prospect, idx)
                self.stats['emails_sent'] += 1

            except Exception as e:
                logger.error(f"❌ Erreur traitement {prospect['name']}: {str(e)}")
                self.stats['errors'] += 1
                continue

        # 3. RAPPORT FINAL
        logger.info("\n📊 ÉTAPE 5/5 : Génération du rapport")
        logger.info("="*60)

        self._generate_report()

        logger.info(f"\n{'='*60}")
        logger.info(f"✅ PIPELINE TERMINÉ")
        logger.info(f"{'='*60}")

        return True

    def scrape_google_maps(self, sector, city, max_results, headless=True):
        """
        SEGMENT 1 : Scraping Google Maps

        Args:
            sector: Type d'établissement
            city: Ville
            max_results: Nombre max de résultats
            headless: Mode headless du navigateur

        Returns:
            list: Liste des prospects trouvés
        """
        logger.info(f"🔍 Recherche: {sector} à {city}")

        self.maps_scraper = GoogleMapsScraper(headless=headless)

        try:
            prospects = self.maps_scraper.search(sector, city, max_results)
            self.stats['total'] = len(prospects)

            # Compter avec/sans site
            for p in prospects:
                if p.get('website'):
                    self.stats['with_website'] += 1
                else:
                    self.stats['without_website'] += 1

            logger.info(f"\n📊 Résultats:")
            logger.info(f"   Total: {len(prospects)}")
            logger.info(f"   Avec site web: {self.stats['with_website']}")
            logger.info(f"   Sans site web: {self.stats['without_website']}")

            return prospects

        finally:
            if self.maps_scraper:
                self.maps_scraper.close()

    def process_prospect(self, prospect, prospect_id):
        """
        Traite un prospect individuel

        Args:
            prospect: Données du prospect (Google Maps)
            prospect_id: ID numérique du prospect
        """
        client_id = f"{prospect_id:03d}"
        has_website = bool(prospect.get('website'))

        logger.info(f"Type: {'AVEC site' if has_website else 'SANS site'}")

        # Données à utiliser pour la génération
        business_data = {
            'id': client_id,
            'name': prospect['name'],
            'address': prospect.get('address', ''),
            'phone': prospect.get('phone', ''),
            'rating': prospect.get('rating'),
            'reviews_count': prospect.get('reviews_count'),
            'category': prospect.get('category', ''),
            'google_maps_url': prospect.get('google_maps_url', '')
        }

        # Déterminer le secteur
        sector = self._detect_sector(prospect.get('category', ''))

        if has_website:
            # AVEC SITE WEB
            screenshots = self._process_with_website(prospect, client_id, sector, business_data)
        else:
            # SANS SITE WEB
            screenshots = self._process_without_website(prospect, client_id, sector, business_data)

        if not screenshots:
            raise Exception("Échec génération screenshots")

        # Génération PDF
        logger.info("📄 Génération PDF...")
        pdf_path = self.pdf_generator.generate_proposal(
            client_id,
            business_data,
            screenshots,
            has_website
        )

        if not pdf_path:
            raise Exception("Échec génération PDF")

        # Envoi email
        to_email = prospect.get('email')

        if not to_email:
            logger.warning(f"⚠️  Pas d'email pour {prospect['name']}, PDF généré mais pas envoyé")
            logger.info(f"   PDF: {pdf_path}")
            return

        logger.info(f"📧 Envoi email à {to_email}...")
        success = self.email_sender.send_proposal(
            to_email,
            business_data,
            pdf_path,
            has_website=has_website
        )

        if success:
            logger.info(f"✅ Prospect traité avec succès")
        else:
            raise Exception("Échec envoi email")

        # Nettoyage
        self.file_manager.cleanup_client_temp(client_id)

    def _process_with_website(self, prospect, client_id, sector, business_data):
        """Traite un prospect qui a déjà un site web"""
        logger.info("🌐 Scraping du site web...")

        # Scraper le site
        web_scraper = WebsiteScraper(client_id, prospect['website'])
        site_data = web_scraper.scrape()

        if not site_data:
            logger.warning("⚠️  Échec scraping, utilisation données Google Maps")
            site_data = {}

        # Extraire les couleurs du logo
        colors = None
        if site_data.get('logo'):
            logger.info("🎨 Extraction couleurs du logo...")
            colors = self.color_extractor.extract_from_logo(site_data['logo'])

        if not colors:
            colors = self.color_extractor.get_default_palette(sector)

        # Préparer les données pour le template
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

        # Générer HTML
        logger.info("🎨 Génération HTML...")
        html_path = self.html_generator.generate(client_id, sector, template_data, colors)

        if not html_path:
            raise Exception("Échec génération HTML")

        # Screenshots
        logger.info("📸 Capture screenshots...")
        screenshots = self.screenshot_maker.capture_website(html_path, client_id, "generated")

        # Ajouter le screenshot original
        if site_data.get('screenshot_original'):
            screenshots['screenshot_original'] = site_data['screenshot_original']

        return screenshots

    def _process_without_website(self, prospect, client_id, sector, business_data):
        """Traite un prospect sans site web"""
        logger.info("🤖 Génération contenu IA...")

        # Générer le contenu avec IA
        ai_content = self.content_generator.generate_website_content(
            business_data['name'],
            business_data['category'],
            business_data['address'].split(',')[-1].strip()  # Ville
        )

        # Couleurs par défaut pour le secteur
        colors = self.color_extractor.get_default_palette(sector)

        # Préparer les données pour le template
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

        # Générer HTML
        logger.info("🎨 Génération HTML...")
        html_path = self.html_generator.generate(client_id, sector, template_data, colors)

        if not html_path:
            raise Exception("Échec génération HTML")

        # Screenshots
        logger.info("📸 Capture screenshots...")
        screenshots = self.screenshot_maker.capture_website(html_path, client_id, "generated")

        return screenshots

    def _detect_sector(self, category):
        """Détecte le secteur depuis la catégorie Google Maps"""
        category_lower = category.lower()

        # Mapping simple
        if 'coif' in category_lower or 'salon' in category_lower or 'beauté' in category_lower:
            return 'beaute'
        elif 'plomb' in category_lower or 'électric' in category_lower or 'menuiserie' in category_lower:
            return 'artisan'
        elif 'restaurant' in category_lower or 'café' in category_lower or 'boulangerie' in category_lower:
            return 'restauration'
        elif 'médecin' in category_lower or 'dentist' in category_lower or 'kiné' in category_lower:
            return 'sante'
        else:
            return 'commerce'

    def _save_prospects_csv(self, prospects, filepath):
        """Sauvegarde les prospects en CSV"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'id', 'name', 'address', 'phone', 'website', 'rating',
                'reviews_count', 'category', 'google_maps_url'
            ])

            writer.writeheader()
            for p in prospects:
                writer.writerow(p)

        logger.info(f"💾 Liste prospects sauvegardée: {filepath}")

    def _generate_report(self):
        """Génère le rapport final"""
        report_path = self.file_manager.get_output_path(
            'report',
            f"rapport_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.txt"
        )

        report = f"""
{'='*60}
RAPPORT D'EXÉCUTION
{'='*60}

Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

STATISTIQUES:
  Total prospects traités: {self.stats['total']}
  - Avec site web:         {self.stats['with_website']}
  - Sans site web:         {self.stats['without_website']}

  Emails envoyés:          {self.stats['emails_sent']}
  Erreurs:                 {self.stats['errors']}

  Taux de succès: {(self.stats['emails_sent'] / self.stats['total'] * 100) if self.stats['total'] > 0 else 0:.1f}%

CONFIGURATION:
  Secteur: {getattr(self, 'sector', 'N/A')}
  Ville: {getattr(self, 'city', 'N/A')}
  Max prospects/jour: {settings.MAX_PROSPECTS_PER_DAY}
  Délai entre emails: {settings.DELAY_BETWEEN_EMAILS}s
  IA activée (sans site): {settings.USE_AI_FOR_NO_SITE}

{'='*60}
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info(f"\n{report}")
        logger.info(f"📊 Rapport sauvegardé: {report_path}")


def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(
        description='Agent de prospection automatisée',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:

  # Pipeline complet (50 prospects)
  python main.py --secteur "coiffeur" --ville "Paris" --limite 50

  # Test avec seulement 5 prospects
  python main.py --secteur "restaurant" --ville "Lyon" --limite 5

  # Segmentsindividuels (debug)
  python main.py --segment google-maps --secteur "plombier" --ville "Marseille"
  python main.py --segment process-one --prospect-file data/prospects/prospects_2025-01-10.csv --index 0

Segments disponibles:
  - google-maps : Scraping Google Maps uniquement
  - process-one : Traiter un seul prospect
  - full        : Pipeline complet (défaut)
        """
    )

    parser.add_argument('--secteur', type=str, help='Secteur activité (ex: coiffeur)')
    parser.add_argument('--ville', type=str, help='Ville')
    parser.add_argument('--limite', type=int, default=50, help='Nombre max de prospects')
    parser.add_argument('--segment', type=str, default='full', choices=['full', 'google-maps', 'process-one'], help='Segment à exécuter')
    parser.add_argument('--headless', action='store_true', help='Mode headless (navigateur invisible)')
    parser.add_argument('--prospect-file', type=str, help='Fichier CSV de prospects (pour segment process-one)')
    parser.add_argument('--index', type=int, default=0, help='Index du prospect à traiter (pour segment process-one)')

    args = parser.parse_args()

    # Créer l'agent
    agent = ProspectAgent()

    # Exécuter selon le segment
    if args.segment == 'full':
        if not args.secteur or not args.ville:
            parser.error("--secteur et --ville requis pour pipeline complet")

        agent.sector = args.secteur
        agent.city = args.ville
        agent.run_full_pipeline(args.secteur, args.ville, args.limite)

    elif args.segment == 'google-maps':
        if not args.secteur or not args.ville:
            parser.error("--secteur et --ville requis pour scraping Google Maps")

        prospects = agent.scrape_google_maps(args.secteur, args.ville, args.limite, args.headless)

        # Sauvegarder
        prospects_file = agent.file_manager.get_prospects_file()
        agent._save_prospects_csv(prospects, prospects_file)

    elif args.segment == 'process-one':
        if not args.prospect_file:
            parser.error("--prospect-file requis pour segment process-one")

        # Charger le fichier CSV
        import csv
        with open(args.prospect_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            prospects = list(reader)

        if args.index >= len(prospects):
            logger.error(f"❌ Index {args.index} hors limites (max: {len(prospects)-1})")
            return

        prospect = prospects[args.index]
        logger.info(f"Traitement prospect: {prospect['name']}")

        agent.process_prospect(prospect, args.index + 1)


if __name__ == "__main__":
    main()
