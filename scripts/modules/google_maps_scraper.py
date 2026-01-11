"""
Scraper Google Maps pour récupérer les établissements
"""
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from scripts.utils.logger import setup_logger
from config import settings

logger = setup_logger("google_maps")


class GoogleMapsScraper:
    """Scraper pour Google Maps"""

    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.page = None
        self.proxy_config = self._get_proxy_config()

    def _get_proxy_config(self):
        """Configure le proxy si nécessaire"""
        if settings.HTTP_PROXY or settings.HTTPS_PROXY:
            proxy_url = settings.HTTPS_PROXY or settings.HTTP_PROXY
            logger.info(f"🌐 Proxy configuré: {proxy_url}")
            return {"server": proxy_url}
        return None

    def start(self):
        """Démarre le navigateur"""
        logger.info("🚀 Démarrage du navigateur...")

        playwright = sync_playwright().start()

        browser_args = {
            "headless": self.headless,
            "args": [
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        }

        if self.proxy_config:
            browser_args["proxy"] = self.proxy_config

        self.browser = playwright.chromium.launch(**browser_args)

        context_args = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "viewport": {"width": 1920, "height": 1080}
        }

        if not settings.VERIFY_SSL:
            logger.warning("⚠️  Vérification SSL désactivée")
            context_args["ignore_https_errors"] = True

        context = self.browser.new_context(**context_args)
        self.page = context.new_page()

        logger.info("✅ Navigateur démarré")

    def search(self, query, city, max_results=50):
        """
        Recherche des établissements sur Google Maps

        Args:
            query: Type d'établissement (ex: "coiffeur")
            city: Ville (ex: "Paris")
            max_results: Nombre max de résultats

        Returns:
            Liste de dictionnaires avec les infos des établissements
        """
        if not self.page:
            self.start()

        search_query = f"{query} {city}"
        logger.info(f"🔍 Recherche: {search_query}")

        # URL Google Maps
        url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"

        try:
            self.page.goto(url, wait_until="networkidle", timeout=60000)
            time.sleep(3)

            # Scroll pour charger plus de résultats
            results_panel = 'div[role="feed"]'
            self._scroll_results_panel(results_panel, max_results)

            # Extraire les établissements
            businesses = self._extract_businesses(max_results)

            logger.info(f"✅ {len(businesses)} établissements trouvés")
            return businesses

        except PlaywrightTimeout:
            logger.error("❌ Timeout lors de la recherche Google Maps")
            return []
        except Exception as e:
            logger.error(f"❌ Erreur lors de la recherche: {str(e)}")
            return []

    def _scroll_results_panel(self, selector, target_count):
        """Scroll le panneau de résultats pour charger plus d'établissements"""
        logger.info("📜 Scroll des résultats...")

        scroll_count = 0
        max_scrolls = 20

        while scroll_count < max_scrolls:
            # Compter les résultats actuels
            current_count = self.page.locator('div[role="article"]').count()

            if current_count >= target_count:
                logger.debug(f"✅ {current_count} résultats chargés")
                break

            # Scroll
            try:
                self.page.evaluate(f"""
                    document.querySelector('{selector}').scrollBy(0, 5000);
                """)
                time.sleep(2)
                scroll_count += 1
                logger.debug(f"Scroll {scroll_count}/{max_scrolls} - {current_count} résultats")

            except Exception as e:
                logger.debug(f"Fin du scroll: {str(e)}")
                break

    def _extract_businesses(self, max_results):
        """Extrait les informations des établissements"""
        logger.info("📊 Extraction des données...")

        businesses = []
        articles = self.page.locator('div[role="article"]').all()[:max_results]

        for idx, article in enumerate(articles, 1):
            try:
                # Cliquer sur l'établissement pour ouvrir les détails
                article.click()
                time.sleep(1.5)

                # Extraire les données
                business_data = self._extract_business_details(idx)

                if business_data:
                    businesses.append(business_data)
                    logger.debug(f"✓ {idx}/{len(articles)}: {business_data['name']}")

            except Exception as e:
                logger.warning(f"⚠️  Erreur extraction {idx}: {str(e)}")
                continue

        return businesses

    def _extract_business_details(self, client_id):
        """Extrait les détails d'un établissement"""
        data = {"id": f"{client_id:03d}"}

        try:
            # Nom
            try:
                name_elem = self.page.locator('h1').first
                data['name'] = name_elem.inner_text(timeout=3000)
            except:
                data['name'] = "Nom inconnu"

            # Adresse
            try:
                address_btn = self.page.locator('button[data-item-id="address"]').first
                data['address'] = address_btn.get_attribute('aria-label', timeout=3000)
                data['address'] = data['address'].replace('Adresse: ', '')
            except:
                data['address'] = None

            # Téléphone
            try:
                phone_btn = self.page.locator('button[data-item-id*="phone"]').first
                data['phone'] = phone_btn.get_attribute('aria-label', timeout=3000)
                data['phone'] = data['phone'].replace('Téléphone: ', '')
            except:
                data['phone'] = None

            # Site web
            try:
                website_link = self.page.locator('a[data-item-id="authority"]').first
                data['website'] = website_link.get_attribute('href', timeout=3000)
            except:
                data['website'] = None

            # Note
            try:
                rating_elem = self.page.locator('span[role="img"]').first
                rating_text = rating_elem.get_attribute('aria-label', timeout=3000)
                # Parse "4,5 étoiles"
                data['rating'] = rating_text.split()[0].replace(',', '.')
            except:
                data['rating'] = None

            # Nombre d'avis
            try:
                # Chercher le texte avec "avis"
                reviews_elem = self.page.locator('text=/\\d+ avis/').first
                reviews_text = reviews_elem.inner_text(timeout=3000)
                data['reviews_count'] = reviews_text.split()[0]
            except:
                data['reviews_count'] = None

            # Type d'activité (catégorie)
            try:
                category_btn = self.page.locator('button[jsaction*="category"]').first
                data['category'] = category_btn.inner_text(timeout=3000)
            except:
                data['category'] = "Non classé"

            # URL Google Maps
            data['google_maps_url'] = self.page.url

            return data

        except Exception as e:
            logger.error(f"Erreur extraction détails: {str(e)}")
            return None

    def save_to_json(self, businesses, filepath):
        """Sauvegarde les résultats en JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(businesses, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Sauvegardé: {filepath}")

    def close(self):
        """Ferme le navigateur"""
        if self.browser:
            self.browser.close()
            logger.info("🔚 Navigateur fermé")


def main():
    """Test du scraper"""
    import argparse

    parser = argparse.ArgumentParser(description='Scraper Google Maps')
    parser.add_argument('--query', type=str, default='coiffeur', help='Type établissement')
    parser.add_argument('--city', type=str, default='Paris', help='Ville')
    parser.add_argument('--max', type=int, default=10, help='Nombre max résultats')
    parser.add_argument('--headless', action='store_true', help='Mode headless')

    args = parser.parse_args()

    scraper = GoogleMapsScraper(headless=args.headless)

    try:
        results = scraper.search(args.query, args.city, args.max)

        # Afficher les résultats
        print(f"\n{'='*60}")
        print(f"✅ {len(results)} établissements trouvés")
        print(f"{'='*60}\n")

        for business in results:
            print(f"📍 {business['name']}")
            print(f"   Adresse: {business.get('address', 'N/A')}")
            print(f"   Téléphone: {business.get('phone', 'N/A')}")
            print(f"   Site web: {business.get('website', 'N/A')}")
            print(f"   Note: {business.get('rating', 'N/A')} ({business.get('reviews_count', 'N/A')} avis)")
            print(f"   Catégorie: {business.get('category', 'N/A')}")
            print()

        # Sauvegarder
        output_file = Path('outputs/reports/google_maps_test.json')
        output_file.parent.mkdir(parents=True, exist_ok=True)
        scraper.save_to_json(results, output_file)

    finally:
        scraper.close()


if __name__ == "__main__":
    main()
