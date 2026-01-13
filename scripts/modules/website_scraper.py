"""
Scraper de sites web pour extraire contenu, images, logo
"""
import os
import re
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from bs4 import BeautifulSoup
from scripts.utils.logger import setup_logger
from scripts.utils.file_manager import FileManager
from config import settings

logger = setup_logger("website_scraper")


class WebsiteScraper:
    """Scraper pour sites web clients"""

    def __init__(self, client_id, url):
        self.client_id = client_id
        self.url = url
        self.file_manager = FileManager()
        self.client_dir = self.file_manager.create_client_temp_dir(client_id)
        self.data = {}

    def scrape(self):
        """
        Scrappe le site web et retourne les données extraites

        Returns:
            dict: Données du site (logo, images, textes, etc.)
        """
        logger.info(f"🔍 Scraping du site: {self.url}")

        try:
            # Récupérer le HTML avec Playwright (pour sites JS)
            html_content, screenshot_path = self._fetch_with_playwright()

            if not html_content:
                logger.error(f"❌ Impossible de récupérer le site: {self.url}")
                return None

            # Parser avec BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extraire les données
            self.data['url'] = self.url
            self.data['screenshot_original'] = screenshot_path
            self.data['logo'] = self._extract_logo(soup)
            self.data['logo_url'] = self._extract_logo_url(soup)
            self.data['title'] = self._extract_title(soup)
            self.data['description'] = self._extract_description(soup)
            self.data['headings'] = self._extract_headings(soup)
            self.data['images'] = self._extract_images(soup)
            self.data['image_urls'] = self._extract_image_urls(soup)
            self.data['texts'] = self._extract_texts(soup)
            self.data['phone'] = self._extract_phone(soup)
            self.data['email'] = self._extract_email(soup)
            self.data['structure'] = self._extract_structure(soup)

            logger.info(f"✅ Site scrappé avec succès")
            return self.data

        except Exception as e:
            logger.error(f"❌ Erreur scraping: {str(e)}")
            return None

    def _fetch_with_playwright(self):
        """Récupère le contenu avec Playwright (gère JS)"""
        playwright = sync_playwright().start()

        browser_args = {
            "headless": True,
            "args": ['--disable-blink-features=AutomationControlled']
        }

        # Proxy si configuré
        if settings.HTTP_PROXY or settings.HTTPS_PROXY:
            proxy_url = settings.HTTPS_PROXY or settings.HTTP_PROXY
            browser_args["proxy"] = {"server": proxy_url}

        browser = playwright.chromium.launch(**browser_args)

        context_args = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        if not settings.VERIFY_SSL:
            context_args["ignore_https_errors"] = True

        context = browser.new_context(**context_args)
        page = context.new_page()

        try:
            page.goto(self.url, wait_until="networkidle", timeout=30000)
            html_content = page.content()

            # Screenshot du site original (pour le AVANT)
            screenshot_path = self.client_dir / "screenshot_original.png"
            page.screenshot(path=str(screenshot_path), full_page=True)

            browser.close()
            playwright.stop()

            return html_content, str(screenshot_path)

        except PlaywrightTimeout:
            logger.warning("⚠️  Timeout - tentative avec requests...")
            browser.close()
            playwright.stop()

            # Fallback: requests simple
            try:
                response = requests.get(
                    self.url,
                    timeout=10,
                    verify=settings.VERIFY_SSL,
                    proxies=settings.PROXIES if settings.PROXIES else None
                )
                return response.text, None
            except:
                return None, None

        except Exception as e:
            logger.error(f"Erreur Playwright: {str(e)}")
            browser.close()
            playwright.stop()
            return None, None

    def _extract_logo(self, soup):
        """Extrait et télécharge le logo"""
        logo_url = None

        # Chercher le logo (plusieurs stratégies)
        # 1. Balise avec "logo" dans class ou id
        logo_elem = soup.find(['img', 'a'], class_=re.compile(r'logo', re.I))
        if not logo_elem:
            logo_elem = soup.find(['img', 'a'], id=re.compile(r'logo', re.I))

        # 2. Premier img dans le header
        if not logo_elem:
            header = soup.find('header')
            if header:
                logo_elem = header.find('img')

        # 3. Première image du site
        if not logo_elem:
            logo_elem = soup.find('img')

        # Récupérer l'URL
        if logo_elem:
            if logo_elem.name == 'img':
                logo_url = logo_elem.get('src')
            elif logo_elem.name == 'a':
                img = logo_elem.find('img')
                if img:
                    logo_url = img.get('src')

        if logo_url:
            # URL absolue
            logo_url = urljoin(self.url, logo_url)

            # Télécharger
            logo_path = self._download_image(logo_url, 'logo.png')
            return str(logo_path) if logo_path else None

        return None

    def _extract_logo_url(self, soup):
        """Extrait l'URL du logo (sans télécharger)"""
        logo_url = None

        # Chercher le logo (plusieurs stratégies)
        # 1. Balise avec "logo" dans class ou id
        logo_elem = soup.find(['img', 'a'], class_=re.compile(r'logo', re.I))
        if not logo_elem:
            logo_elem = soup.find(['img', 'a'], id=re.compile(r'logo', re.I))

        # 2. Premier img dans le header
        if not logo_elem:
            header = soup.find('header')
            if header:
                logo_elem = header.find('img')

        # 3. Première image du site
        if not logo_elem:
            logo_elem = soup.find('img')

        # Récupérer l'URL
        if logo_elem:
            if logo_elem.name == 'img':
                logo_url = logo_elem.get('src')
            elif logo_elem.name == 'a':
                img = logo_elem.find('img')
                if img:
                    logo_url = img.get('src')

        if logo_url:
            # URL absolue
            logo_url = urljoin(self.url, logo_url)
            return logo_url

        return None

    def _extract_title(self, soup):
        """Extrait le titre principal"""
        # H1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)

        # Title tag
        title = soup.find('title')
        if title:
            return title.get_text(strip=True)

        return "Site web"

    def _extract_description(self, soup):
        """Extrait la description/slogan"""
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')

        # Premier paragraphe
        p = soup.find('p')
        if p:
            return p.get_text(strip=True)[:200]

        return ""

    def _extract_headings(self, soup):
        """Extrait tous les headings"""
        headings = []
        for tag in ['h1', 'h2', 'h3']:
            for elem in soup.find_all(tag, limit=5):
                text = elem.get_text(strip=True)
                if text and len(text) > 3:
                    headings.append(text)
        return headings

    def _extract_images(self, soup):
        """Extrait et télécharge les images principales"""
        images = []
        img_tags = soup.find_all('img', limit=10)

        for idx, img in enumerate(img_tags):
            img_url = img.get('src') or img.get('data-src')
            if not img_url:
                continue

            # Ignorer les petites images (icônes, etc.)
            width = img.get('width')
            height = img.get('height')
            if width and height:
                try:
                    if int(width) < 100 or int(height) < 100:
                        continue
                except:
                    pass

            # URL absolue
            img_url = urljoin(self.url, img_url)

            # Télécharger
            img_path = self._download_image(img_url, f'image_{idx+1}.jpg')
            if img_path:
                images.append(str(img_path))

        return images[:5]  # Max 5 images

    def _extract_image_urls(self, soup):
        """Extrait les URLs des images (sans télécharger)"""
        image_urls = []
        img_tags = soup.find_all('img', limit=10)

        for img in img_tags:
            img_url = img.get('src') or img.get('data-src')
            if not img_url:
                continue

            # Ignorer les petites images (icônes, etc.)
            width = img.get('width')
            height = img.get('height')
            if width and height:
                try:
                    if int(width) < 100 or int(height) < 100:
                        continue
                except:
                    pass

            # URL absolue
            img_url = urljoin(self.url, img_url)
            image_urls.append(img_url)

        return image_urls[:5]  # Max 5 images

    def _extract_texts(self, soup):
        """Extrait les paragraphes de texte"""
        texts = []

        for p in soup.find_all('p', limit=15):
            text = p.get_text(strip=True)
            if text and len(text) > 20:
                texts.append(text)

        return texts

    def _extract_phone(self, soup):
        """Extrait le numéro de téléphone"""
        # Regex téléphone français
        phone_pattern = r'0[1-9](?:[\s.-]*\d{2}){4}'

        # Chercher dans les liens tel:
        tel_link = soup.find('a', href=re.compile(r'tel:', re.I))
        if tel_link:
            return tel_link.get_text(strip=True)

        # Chercher dans le texte
        text = soup.get_text()
        match = re.search(phone_pattern, text)
        if match:
            return match.group(0)

        return None

    def _extract_email(self, soup):
        """Extrait l'email"""
        # Chercher dans les liens mailto:
        mailto_link = soup.find('a', href=re.compile(r'mailto:', re.I))
        if mailto_link:
            email = mailto_link.get('href').replace('mailto:', '')
            return email

        # Regex email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        text = soup.get_text()
        match = re.search(email_pattern, text)
        if match:
            return match.group(0)

        return None

    def _extract_structure(self, soup):
        """
        Extrait la structure complète du site (ordre, sections, textes complets)
        pour préserver le squelette exact du site
        """
        structure = []

        # Chercher le contenu principal (main, body, ou tags de contenu)
        main_content = soup.find('main') or soup.find('body')

        if not main_content:
            logger.warning("Aucun contenu principal trouvé")
            return structure

        # Parser récursivement les sections
        current_section = None
        section_counter = 0

        for element in main_content.find_all(['section', 'div', 'article', 'h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol'], recursive=False):
            # Ignorer les éléments de navigation, header, footer
            if self._is_navigation_element(element):
                continue

            # Sections principales
            if element.name in ['section', 'article'] or (element.name == 'div' and self._looks_like_section(element)):
                section_counter += 1
                section_data = self._parse_section(element, section_counter)
                if section_data and section_data['content']:
                    structure.append(section_data)

            # Éléments isolés (hors section)
            elif element.name in ['h1', 'h2', 'h3', 'h4', 'p', 'ul', 'ol']:
                if not current_section:
                    section_counter += 1
                    current_section = {
                        'type': 'section',
                        'title': f'Section {section_counter}',
                        'content': []
                    }
                    structure.append(current_section)

                content_item = self._parse_element(element)
                if content_item:
                    current_section['content'].append(content_item)

        logger.info(f"✓ Structure extraite: {len(structure)} sections")
        return structure

    def _is_navigation_element(self, element):
        """Vérifie si un élément est de la navigation"""
        # Navigation, header, footer, sidebar, menu
        nav_keywords = ['nav', 'menu', 'header', 'footer', 'sidebar', 'aside']

        # Vérifier les classes et IDs
        classes = ' '.join(element.get('class', [])).lower()
        elem_id = (element.get('id') or '').lower()

        for keyword in nav_keywords:
            if keyword in classes or keyword in elem_id:
                return True

        return element.name in ['nav', 'header', 'footer', 'aside']

    def _looks_like_section(self, element):
        """Détermine si un div ressemble à une section de contenu"""
        # Div avec beaucoup de contenu texte
        text_length = len(element.get_text(strip=True))
        if text_length < 50:
            return False

        # Div avec des titres
        if element.find(['h1', 'h2', 'h3']):
            return True

        # Div avec des paragraphes
        if len(element.find_all('p')) >= 2:
            return True

        return False

    def _parse_section(self, section_element, section_num):
        """Parse une section complète"""
        section_data = {
            'type': 'section',
            'title': None,
            'content': []
        }

        # Chercher un titre pour la section
        title_elem = section_element.find(['h1', 'h2', 'h3', 'h4'])
        if title_elem:
            section_data['title'] = title_elem.get_text(strip=True)
        else:
            section_data['title'] = f'Section {section_num}'

        # Parser tous les éléments de contenu
        for elem in section_element.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'blockquote']):
            content_item = self._parse_element(elem)
            if content_item:
                section_data['content'].append(content_item)

        return section_data

    def _parse_element(self, element):
        """Parse un élément individuel (titre, paragraphe, liste)"""
        elem_type = element.name

        # Titres
        if elem_type in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            text = element.get_text(strip=True)
            if text and len(text) > 0:
                return {
                    'type': 'heading',
                    'level': elem_type,
                    'text': text
                }

        # Paragraphes
        elif elem_type == 'p':
            text = element.get_text(strip=True)
            if text and len(text) > 10:  # Ignorer les paragraphes trop courts
                return {
                    'type': 'paragraph',
                    'text': text
                }

        # Listes
        elif elem_type in ['ul', 'ol']:
            items = []
            for li in element.find_all('li', recursive=False):
                item_text = li.get_text(strip=True)
                if item_text:
                    items.append(item_text)

            if items:
                return {
                    'type': 'list',
                    'ordered': elem_type == 'ol',
                    'items': items
                }

        # Citations
        elif elem_type == 'blockquote':
            text = element.get_text(strip=True)
            if text:
                return {
                    'type': 'quote',
                    'text': text
                }

        return None

    def _download_image(self, url, filename):
        """Télécharge une image"""
        try:
            response = requests.get(
                url,
                timeout=10,
                verify=settings.VERIFY_SSL,
                proxies=settings.PROXIES if settings.PROXIES else None,
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            if response.status_code == 200:
                filepath = self.client_dir / filename

                with open(filepath, 'wb') as f:
                    f.write(response.content)

                logger.debug(f"✓ Image téléchargée: {filename}")
                return filepath

        except Exception as e:
            logger.debug(f"⚠️  Erreur téléchargement image: {str(e)}")

        return None


def main():
    """Test du scraper"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Scraper de site web')
    parser.add_argument('--url', type=str, required=True, help='URL du site à scraper')
    parser.add_argument('--client-id', type=str, default='test', help='ID client')

    args = parser.parse_args()

    scraper = WebsiteScraper(args.client_id, args.url)
    data = scraper.scrape()

    if data:
        print(f"\n{'='*60}")
        print(f"✅ Site scrappé: {args.url}")
        print(f"{'='*60}\n")

        print(f"Titre: {data.get('title')}")
        print(f"Description: {data.get('description')}")
        print(f"Logo: {data.get('logo')}")
        print(f"Téléphone: {data.get('phone')}")
        print(f"Email: {data.get('email')}")
        print(f"\nImages trouvées: {len(data.get('images', []))}")
        print(f"Textes extraits: {len(data.get('texts', []))}")

        # Sauvegarder
        output_file = Path(f'outputs/reports/scraping_{args.client_id}.json')
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Données sauvegardées: {output_file}")

    else:
        print("❌ Échec du scraping")


if __name__ == "__main__":
    main()
